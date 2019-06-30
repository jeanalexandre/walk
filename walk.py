from time import sleep
import RPi.GPIO as GPIO
import time

#DEF PIN GPIO MOTEURS
MOTOR1_EN = 14
MOTOR1_A = 15
MOTOR1_B = 18

MOTOR2_EN = 25
MOTOR2_A = 7
MOTOR2_B = 8

#DEF PIN GPIO SENSORS

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Left sensor
TRIG_LEFT = 19
ECHO_LEFT = 13


# Front sensor 
TRIG_FRONT = 6
ECHO_FRONT = 5

# Right sensor 
TRIG_RIGHT = 21
ECHO_RIGHT = 20

GPIO.setup(TRIG_LEFT,GPIO.OUT)
GPIO.setup(TRIG_FRONT,GPIO.OUT)
GPIO.setup(TRIG_RIGHT,GPIO.OUT)
GPIO.setup(ECHO_LEFT,GPIO.IN)
GPIO.setup(ECHO_FRONT,GPIO.IN)
GPIO.setup(ECHO_RIGHT,GPIO.IN)

#FUNCTIONS

# Retourne la distance mesurée par le capteur de gauche
def left_mesure():
    GPIO.output(TRIG_LEFT,False)
    time.sleep(0.5)

    #Declenchement du TRIG en le mettant en etat haut durant 1µs
    GPIO.output(TRIG_LEFT,True)
    time.sleep(0.00001)
    GPIO.output(TRIG_LEFT,False)

    while GPIO.input(ECHO_LEFT)==0:
        pulse_start_L = time.time()
        
    while GPIO.input(ECHO_LEFT)==1:
        pulse_end_L = time.time()

    pulse_duration_L = pulse_end_L - pulse_start_L

    distance_L = pulse_duration_L * 17150

    distance_L = round(distance_L,2)

    #print("Distance gauche: ", distance_L, " cm")
    
    return distance_L

# Retourne la distance mesurée par le capteur de devant
def front_mesure():
    GPIO.output(TRIG_FRONT,False)
    time.sleep(0.5)

    #Declenchement du TRIG en le mettant en etat haut durant 1µs
    GPIO.output(TRIG_FRONT,True)
    time.sleep(0.00001)
    GPIO.output(TRIG_FRONT,False)

    while GPIO.input(ECHO_FRONT)==0:
        pulse_start_F = time.time()
        
    while GPIO.input(ECHO_FRONT)==1:
        pulse_end_F = time.time()

    pulse_duration_F = pulse_end_F - pulse_start_F

    distance_F = pulse_duration_F * 17150

    distance_F = round(distance_F,2)

    #print("Distance devant: ", distance_F, " cm")
    
    return distance_F

# Retourne la distance mesurée par le capteur de droite
def right_mesure():
    GPIO.output(TRIG_RIGHT,False)
    time.sleep(0.5)

    #Declenchement du TRIG en le mettant en etat haut durant 1µs
    GPIO.output(TRIG_RIGHT,True)
    time.sleep(0.00001)
    GPIO.output(TRIG_RIGHT,False)

    while GPIO.input(ECHO_RIGHT)==0:
        pulse_start_R = time.time()
        
    while GPIO.input(ECHO_RIGHT)==1:
        pulse_end_R = time.time()

    pulse_duration_R = pulse_end_R - pulse_start_R

    distance_R = pulse_duration_R * 17150

    distance_R = round(distance_R,2)

    #print("Distance droite: ", distance_R, " cm")
    
    return distance_R

    
def arriere(duree):
    
    GPIO.setup(MOTOR1_EN, GPIO.OUT)
    GPIO.setup(MOTOR1_A, GPIO.OUT)
    GPIO.setup(MOTOR1_B, GPIO.OUT)
    
    GPIO.setup(MOTOR2_EN, GPIO.OUT)
    GPIO.setup(MOTOR2_A, GPIO.OUT)
    GPIO.setup(MOTOR2_B, GPIO.OUT)
    
    motor1GPIO = GPIO.PWM(MOTOR1_EN, 100)
    motor2GPIO = GPIO.PWM(MOTOR2_EN, 100)
    
    #RECULER
   #print("je recule")
    """Fait avancer le robot en faisant tourner
    les deux moteurs du meme sens"""
    motor1GPIO.start(100)
    GPIO.output(MOTOR1_A, GPIO.HIGH)
    GPIO.output(MOTOR1_B, GPIO.LOW)
    
    motor2GPIO.start(100)
    GPIO.output(MOTOR2_A, GPIO.HIGH)
    GPIO.output(MOTOR2_B, GPIO.LOW)
    
    #Continue d'avancer pendant x seconde
    sleep(duree)
    
    motor1GPIO.stop()
    motor2GPIO.stop()
    
def avant():
    
    GPIO.setup(MOTOR1_EN, GPIO.OUT)
    GPIO.setup(MOTOR1_A, GPIO.OUT)
    GPIO.setup(MOTOR1_B, GPIO.OUT)
    
    GPIO.setup(MOTOR2_EN, GPIO.OUT)
    GPIO.setup(MOTOR2_A, GPIO.OUT)
    GPIO.setup(MOTOR2_B, GPIO.OUT)
    
    motor1GPIO = GPIO.PWM(MOTOR1_EN, 100)
    motor2GPIO = GPIO.PWM(MOTOR2_EN, 100)
    
    #AVANCER
    #print("j'avance")
    """Fait avancer le robot en faisant tourner
    les deux moteurs du meme sens"""
    motor1GPIO.start(100)
    GPIO.output(MOTOR1_A, GPIO.LOW)
    GPIO.output(MOTOR1_B, GPIO.HIGH)
    
    motor2GPIO.start(100)
    GPIO.output(MOTOR2_A, GPIO.LOW)
    GPIO.output(MOTOR2_B, GPIO.HIGH)
    
    while front_mesure() > 15 and right_mesure() > 5 and left_mesure() > 5:
        pass
    
    motor1GPIO.stop()
    motor2GPIO.stop()
    
    
def droite():
    
    GPIO.setup(MOTOR1_EN, GPIO.OUT)
    GPIO.setup(MOTOR1_A, GPIO.OUT)
    GPIO.setup(MOTOR1_B, GPIO.OUT)
    
    GPIO.setup(MOTOR2_EN, GPIO.OUT)
    GPIO.setup(MOTOR2_A, GPIO.OUT)
    GPIO.setup(MOTOR2_B, GPIO.OUT)
    
    motor1GPIO = GPIO.PWM(MOTOR1_EN, 100)
    motor2GPIO = GPIO.PWM(MOTOR2_EN, 100)
    #TOURNER A GAUCHE
    #print("je tourne à droite")
    """Fait tourner le robot à gauche en faisant tourner
    les deux moteurs à sens opposé"""
    
    motor1GPIO.start(100)
    GPIO.output(MOTOR1_A, GPIO.LOW)
    GPIO.output(MOTOR1_B, GPIO.HIGH)
    
    motor2GPIO.start(100)
    GPIO.output(MOTOR2_A, GPIO.HIGH)
    GPIO.output(MOTOR2_B, GPIO.LOW)
    
    while front_mesure() < 15 or right_mesure() < 15 :
        pass
    
    #Stop et freine les moteur
    motor1GPIO.stop()
    motor2GPIO.stop()
    
def walk():
    while 1:
        avant()
        droite()
     
#LOGIC
        
try:
    walk()
    
except KeyboardInterrupt:
    pass
except:
    GPIO.cleanup()
    raise

GPIO.cleanup()