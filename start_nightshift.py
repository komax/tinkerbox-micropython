import machine
import utime

from nightshift import Time, Nightshift
import neupixel

def localtime2time():
    current_time = utime.localtime()
    return Time(hour=current_time[3], minute=current_time[4])


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("I woke from a deep sleep")


white_noise_color = 255, 147, 41


pixel = neupixel.create_neu_pixel(pin=16, num_pixels=16)


def light_up(duration):
    pixel.set_color(*white_noise_color)
    utime.sleep(duration)
    pixel.clear()

ns = Nightshift(begin=Time(19, 30), end=Time(22, 30))


print("Localtime: {}".format(utime.localtime()))
current_time = localtime2time()

if ns.is_at_begin(current_time) or ns.is_within(current_time):
    print("I set neopixel with {}".format(white_noise_color))
    # Within night shift, light up
    pixel.set_color(*white_noise_color)
else:
    print("Clearing neopixel's color")
    # Otherwise don't show anything.
    pixel.clear()
# Calculate the sleep time.
sleeptime = ns.sleep_time(current_time, max_sleep=Time(6, 0))
print("I am going to sleep for {}".format(sleeptime))
#utime.sleep(60 * sleeptime)
machine.deepsleep(1_000 * 60 * sleeptime)

