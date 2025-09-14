from periphery import GPIO
import time

# %% LED闪烁
def cycle(led, step):
    # Light
    led.write(True)
    time.sleep(step)
    # Drak
    led.write(False)
    time.sleep(step)
    return

def main():
    led = GPIO(3, "out")
    print("Fading LED on GPIO 3 (press CTRL+C to stop)")
    try:
        while True:
            cycle(led, 0.2)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        led.write(False)
        led.close()

# %% 呼吸灯
def pwm_cycle(gpio, duty):
    # Run a single PWM cycle
    PWM_PERIOD = 1.5
    on_time = PWM_PERIOD * duty
    off_time = PWM_PERIOD - on_time
    gpio.write(True)
    time.sleep(on_time)
    gpio.write(False)
    time.sleep(off_time)
    return

def main():
    gpio = GPIO(3, "out")
    print("Fading LED on GPIO 3 using software PWM (press CTRL+C to stop)...")
    try:
        while True:
            # Fade in
            STEPS = 50 # 渐变步数，越多越平滑
            for i in range(STEPS):
                duty = i / (STEPS - 1)
                pwm_cycle(gpio, duty)
            # Fade out
            for i in reversed(range(STEPS)):
                duty = i / (STEPS - 1)
                pwm_cycle(gpio, duty)
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        gpio.write(False)
        gpio.close()