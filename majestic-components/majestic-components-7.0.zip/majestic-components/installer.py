import os

print("Setting Up Majestic Pi Components....")
os.chdir("/etc/init.d")
os.system("sudo wget -O asplashscreen https://dl-web.dropbox.com/get/majesticpi/components/asplashscreen")
print("Setting Up Splash Screen....")
with open("/boot/cmdline.txt", "a") as myfile:
    myfile.write(" quiet")
os.system("sudo chmod a+x /etc/init.d/asplashscreen")
os.system("sudo insserv /etc/init.d/asplashscreen")

answer = input("Are You Using The Majestic Pi Set Top Box? (y/n)")
if answer == "y":
    print("Gathering The Majestic Pi OS....")
elif answer == "n":
    print("All Done! Enjoy!")
else:
    print("Invalid Answer?!?")
    print("Will Not Install The OS. To Install, Run Again And Answer 'y'.")


