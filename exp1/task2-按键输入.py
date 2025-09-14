from periphery import GPIO
import time

# %% 按键控制LED明灭
def main():
    button = GPIO(2, "in")
    button.edge = "falling"
    led = GPIO(3, "out")
    try:
        while True:
            print("Waiting for button press...")
            if button.poll(timeout = None):
                print("Button pressed!")

                # 明->灭
                if (led.read()):
                    led.write(False)
                    
                # 灭->明
                else:
                    led.write(True)
                    
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        led.write(False)
        led.close()

# %% 按键控制闪烁频率
def cycle(led, step):
    # Light
    led.write(True)
    time.sleep(step)
    # Drak
    led.write(False)
    time.sleep(step)
    return

def main():
    button = GPIO(2, "in")
    button.edge = "falling"
    led = GPIO(3, "out")
    double_click_time = 0.5
    click_times = []  # 存储按键按下的时间戳
    try:
        while True:
            step = 1
            print("Waiting for button press...")
            if button.poll(timeout = None):
                print("Button pressed!")

                # 记录当前按键按下的时间
                current_time = time.time()
                click_times.append(current_time)

                # 只保留最近的两次按键时间
                if len(click_times) > 2:
                    click_times.pop(0)
                
                # 检查是否双击
                if len(click_times) == 2:
                    time_diff = click_times[1] - click_times[0]
                    if time_diff <= double_click_time:
                        print(f"检测到双击！时间间隔: {time_diff:.3f}秒，停止闪烁！")
                        # 停止LED闪烁
                        led.write(False)
                        # 清空记录，避免连续检测
                        click_times = []

                # 灯已亮，单击闪烁频率加倍
                elif (led.read()):
                    step /= 2
                    cycle(led, step)

                # 灯灭，单击开始闪烁
                else:
                    cycle(led, step)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        led.write(False)
        led.close()
