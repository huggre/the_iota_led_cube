# Import some standard Python libraries
import time
import random

# Import the Raspberry PI GPIO library
import RPi.GPIO as GPIO

# Import the PyZMQ library
import zmq

# Define some ZMQ objects 
context = zmq.Context()
socket = context.socket(zmq.SUB)

# Subscribe to all new and confirmed transaction events
socket.setsockopt(zmq.SUBSCRIBE, b'tx')
socket.setsockopt(zmq.SUBSCRIBE, b'sn')

# Specify IRI node from where to get the ZMQ stream
# IMPORTANT!! IRI node must have ZMQ enabled
socket.connect('tcp://zmq.devnet.iota.org:5556')

# Prepare GPIO board
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define list of vertical LEDCube grids
GRID = [7,11,35,37,12,13,31,33,15,16,23,29,18,19,21,22]

# Define list of horizontal LEDCube layers
LAYER = [40,38,36,32]

# Setup layers
GPIO.setup(32, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

# Setup individual LED's
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

# Function to flash a random LED
def flash_led():
    
    # Get random LED
    layer_led = random.choice(LAYER)
    grid_led = random.choice(GRID)
        
    # Turn on LED
    GPIO.output(layer_led,True)
    GPIO.output(grid_led,True)
    
    # Keep LED on for 0.05 seconds
    time.sleep(0.05)
    
    # Turn off LED
    GPIO.output(layer_led,False)
    GPIO.output(grid_led,False)


# Funtion to reset all grid LED's
def reset(x):
        for i in range(0,16):
            GPIO.output(GRID[i],False)

# Funtion to reset all layer LED's
def resetlayer(x):
    for i in range(0,4):
        GPIO.output(LAYER[i],False)

# Make sure all LED's are off before we start...
reset(GRID)
resetlayer(LAYER)

try:
    while(True):
        
        # Get ZMQ event
        topic, data = socket.recv().decode().split(' ', 1)
        
        # If ZMQ event is new transaction
        if topic == 'tx':
            tx_hash, address, value, obs_tag, ts, index, lastindex, \
            bundle_hash, trunk_hash, branch_hash, received_ts, tag = data.split(' ')
            
            # Print transaction data to terminal
            print('NEW TRANSACTION:\n\nAddress: %s\nTransaction hash: %s\nValue: %di \nTag: %s\n' % (address, tx_hash, int(value), tag))

            # Flash random LEDCube LED
            flash_led()

        
except KeyboardInterrupt:
    GPIO.cleanup()
