# NUCLEO-G431RB 基础实验

> **核心命题**　在跑电机之前，先用六个经典小实验把 G431 的"通用功"练熟：GPIO 点灯、定时器 PWM、外部中断、串口、DAC、互补 PWM。它们分别对应电机控制系统的一个零件——状态指示、占空比生成、按钮控制、日志输出、模拟激励、功率桥驱动。本章结束时，驱动电机所需的全部外设都已被单独验证过。

---

**本章实验通用前置**：按 3.3.2 节流程新建工程（Board Selector 选 NUCLEO-G431RB）；每个实验只列出 CubeMX 需要修改的配置与用户代码，其余保持默认。实验结果都用板上现象 + 串口打印验证。

## LED 点灯实验

**目标**：让板载 LD2（绿色，接 PA5）以 1 Hz 闪烁。

**CubeMX 配置**：Pinout 视图中点击 PA5 $\rightarrow$ 选 `GPIO_Output`；System Core $\rightarrow$ GPIO 中确认 PA5 输出电平为 Low、无上下拉、推挽输出。

**用户代码**（`main.c`，写在 `USER CODE BEGIN 3` 循环内）：

```c
while (1)
{
    HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    HAL_Delay(500);          /* ms 级延时，1 Hz 翻转 */
}
```

**现象与验证**：LD2 每秒闪烁一次。把 `TogglePin` 换成 `WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET)` 即常亮——PA5 写 1 点亮，与 UM2079 的描述一致。

![LED 与按键电路：LD2 经限流电阻接 PA5；B1 按下把 PC13 拉低，EXTI13 捕获边沿后经 NVIC 触发中断服务函数](images/fig_04_led_button.pdf)

这个电路图看似简单，却包含了后面所有实验的两种最基本交互：**输出控制**（MCU 决定外设状态）与**输入感知**（MCU 感知外界动作）。

## 定时器 PWM 应用实验

**目标**：在 TIM2 通道 1（PA0）输出 1 kHz、占空比可调的 PWM——这是理解电机驱动"占空比 = 电压指令"的起点。

**定时器三要素**：预分频 PSC、自动重装 ARR、比较 CCR。计数器在每个时钟沿加一，从 0 数到 ARR 后归零（边沿对齐模式）；CNT 与 CCR 比较决定输出电平：

$$f_{PWM} = \frac{f_{TIM}}{(PSC+1)(ARR+1)}, \qquad D = \frac{CCR}{ARR+1}$$

**CubeMX 配置**：Timers $\rightarrow$ TIM2 $\rightarrow$ Slave/Channel1 选 `PWM Generation CH1`；Parameter Settings 里 Prescaler = 169（170 MHz / 170 = 1 MHz 计数）、Counter Period = 999（1 MHz / 1000 = 1 kHz）、Pulse（CCR 初值）= 500。

**用户代码**：

```c
HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
/* 主循环里呼吸灯式修改占空比 */
uint32_t ccr = 0;
while (1) {
    ccr = (ccr + 10) % 1000;
    __HAL_TIM_SET_COMPARE(&htim2, TIM_CHANNEL_1, ccr);
    HAL_Delay(10);
}
```

![定时器 PWM 原理：计数器 0 到 ARR 循环计数，CNT 小于 CCR 期间输出高电平；改 CCR 即改占空比（图中两个周期分别为 70\% 与 40\%）](images/fig_04_pwm_duty.png)

**现象与验证**：示波器（或万用表平均电压档）可见 1 kHz 方波，占空比 0 $\rightarrow$ 100\% 缓慢扫动；把 LED 串电阻接 PA0 可见呼吸效果。**记住这张图**：第 6 章的 SVPWM 最终产物就是三个这样的 PWM 波，只是频率高两个数量级、占空比由算法每周期刷新。

## 外部中断实验

**目标**：按下 B1（PC13）翻转 LED，中断方式实现（不用轮询）。

**CubeMX 配置**：点击 PC13 选 `GPIO_EXTI13`；GPIO 配置里触发沿选 Falling（按下为低）；NVIC 里勾选 `EXTI line 15..10 interrupt` 并给合理抢占优先级（如 5）。

**用户代码**：

```c
/* main.c —— 回调函数（HAL 已在启动文件的中断向量里接管入口） */
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == GPIO_PIN_13) {
        HAL_GPIO_TogglePin(GPIOA, GPIO_PIN_5);
    }
}
```

**现象与验证**：每按一次 B1，LD2 翻转一次。中断路径即图 4.1 右侧：引脚边沿 $\rightarrow$ EXTI13 检测 $\rightarrow$ NVIC 仲裁 $\rightarrow$ `EXTI15_10_IRQHandler`（启动文件中的向量入口）$\rightarrow$ HAL 分发到用户回调。

**为什么用中断**：电机控制的主循环时间预算以微秒计，"等按键"这种事必须让硬件代劳。第 7 章的旋钮控制实验（7.4 节）会把"按键改速度"与"电机控制"并存，靠的就是这套机制。

## 串行接口应用实验

**目标**：printf 经 ST-LINK 虚拟串口上 PC，作为此后所有实验的日志通道。

**CubeMX 配置**：Connectivity $\rightarrow$ USART2 $\rightarrow$ Mode 选 Asynchronous（波特率 115200-8-N-1）。NUCLEO 板上 USART2 的 PA2(TX)/PA3(RX) 已经由 SB13/SB14 焊桥默认路由到 ST-LINK 虚拟串口，不需要飞线。

**UART 帧格式**（异步串口的本质）：空闲态高电平，每字节一帧——起始位（低）+ 8 数据位（LSB 先行）+ 可选校验 + 停止位（高）：

![UART 帧格式（以发送 0x55 为例）：起始位、8 位数据低位先行、停止位](images/fig_04_uart_frame.png)

**用户代码**（GCC/CubeIDE 下重定向 printf）：

```c
#include <stdio.h>
/* retarget printf 到 USART2 —— 记得勾选 -u _printf_float 才能打印浮点 */
int _write(int fd, char *ptr, int len)
{
    HAL_UART_Transmit(&huart2, (uint8_t *)ptr, len, HAL_MAX_DELAY);
    return len;
}

printf("speed = %.1f rpm\r\n", rpm);
```

**现象与验证**：PC 打开任意串口终端（115200）可见打印。**电机实验的纪律**：printf 只放在主循环/低优先级任务里，绝不放进电流环中断——一次浮点 printf 的执行时间足够电流环跑几十拍。

## 数/模转换应用实验

**目标**：用 DAC1 输出正弦波与三角波，验证"数字 $\rightarrow$ 模拟"通路（也是理解 ADC 采样的镜像过程）。

**CubeMX 配置**：Analog $\rightarrow$ DAC1 $\rightarrow$ OUT1（PA4）勾选 External 内部缓冲输出；触发源 TIMER2 TRGO（用 TIM2 TRGO 事件定时更新 DAC）。

**用户代码思路**：正弦查表法（DDS 思想的极简版）：

```c
/* 32 点正弦表，DAC 双极性偏置到中点 */
const uint16_t sine_tab[32] = { 2048, 2447, 2831, ... /* 2048*(1+sin(2πk/32)) */ };

/* TIM2 触发 DAC 时顺序把表值搬到 DHR 寄存器 */
```

![DAC 输出示例：左为正弦查表输出（12-bit 分辨率下的阶梯），右为定时器触发的三角波](images/fig_04_dac_out.png)

**现象与验证**：示波器在 PA4 上看到正弦/三角波，波形频率 = 触发频率 / 表长。**与电机控制的联系**：DAC 在电机板上的标准用法有两个——输出已知模拟量去验证 ADC 采样链路，以及给比较器提供过流阈值（第 7 章的保护机制）。

## 互补 PWM 输出实验

**目标**：用 TIM1 同时输出互补的 CH1/CH1N（带死区、中央对齐）——这是三相逆变桥一个桥臂的完整驱动波形，是本章通往第 5 章的桥。

**为什么需要互补 + 死区**：半桥上下两管绝不允许同时导通（直通 = 短路母线）。理论上一路 PWM 取反就是下管波形，但实际开关管开通/关断有纳秒到微秒级的延迟差异，必须在上管关断与下管开通之间（以及反之）人为插入一段"两管皆关"的死区时间。

**CubeMX 配置**（Timers $\rightarrow$ TIM1）：

- Channel1 选 `PWM Generation CH1 CH1N`（互补输出，引脚默认 PA8/PA7）；
- Counter Mode 选 **Center-aligned mode 1**（中央对齐：计数器上数到 ARR 再下数到 0，一个 PWM 周期 = 一次上数 + 一次下数）；
- Dead Time 按硬件填：例如 170 MHz 计数、1 µs 死区 $\rightarrow$ DeadTime ≈ 170（严格按 RM0440 的 DTG 位定义换算）；
- 20 kHz PWM：$ARR = f_{TIM}/(2 f_{PWM}) - 1 = 170\,\mathrm{MHz}/(2 \times 20\,\mathrm{kHz}) - 1 \approx 4249$。

**用户代码**：

```c
HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);        /* 上管 */
HAL_TIMEx_PWMN_Start(&htim1, TIM_CHANNEL_1);     /* 下管（互补，扩展函数） */
```

![互补 PWM 与死区：上为中央对齐计数器，中为上管 CH1，下为下管 CH1N——每个开关沿两侧都插入两管同时关断的死区（图中放大标出）](images/fig_04_deadtime.png)

**现象与验证**：双通道示波器同时看 PA8/PA7，两路严格反相，且每个边沿附近可见宽度恒定的死区缺口；改 Dead Time 参数，缺口宽度随之变化。

**承上启下**：把 CH1/CH1N 复制到 CH2/CH2N、CH3/CH3N，就是三相逆变桥需要的全部 6 路 PWM；中央对齐 + 谷底触发 ADC 采样 + 刹车输入，合起来就是第 6 \textasciitilde{} 7 章 FOC 电流环的硬件骨架。唯一的差别是：届时占空比不再手工设定，而由 Clarke/Park/PI/SVPWM 流水线每周期自动算出。

## 本章小结

| 实验 | 外设 | 在电机系统中的对应物 |
| --- | --- | --- |
| 点灯 | GPIO 输出 | 状态指示、故障灯 |
| PWM | TIM2 + CCR | 占空比 = 电压指令（SVPWM 的输出形式） |
| 外部中断 | EXTI + NVIC | 按键/保护事件的非阻塞响应 |
| 串口 | USART2 + VCP | 调试日志与上位机通道 |
| DAC | DAC1 + 查表 | ADC 链路验证、比较器阈值 |
| 互补 PWM | TIM1 CH/CHN | 三相半桥驱动的标准波形 |

六个实验的外设配置全部来自 CubeMX 图形界面——这正是第 3 章强调的官方路径：配置交给工具，精力留给算法。

## 本章参考

- UM2079（LD2 = PA5、B1 = PC13、USART2 虚拟串口、供电跳线）
- RM0440 第 21/26/28 章（TIM1 高级定时器 / DAC / 中断与事件）
- STM32CubeG4 官方例程包（NUCLEO-G431RB 的 TIM1 互补输出示例）
