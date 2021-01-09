import b0RemoteApi
import time
from math import *

with b0RemoteApi.RemoteApiClient('b0RemoteApi_pythonClient', 'b0RemoteApi_first') as client:
    doNextStep = True
    flag = True
    adder = 0
    legPos = None


    def simulationStepDone(msg):
        simTime = msg[1][b'simulationTime'];
        global doNextStep
        global flag
        global objHand
        global adder
        global targetLegHand
        global legPos

        adder += 1

        errPose, objPose = client.simxGetObjectPosition(objHand, -1, client.simxServiceCall())
        __e = client.simxSetObjectPosition(
            objHand,
            -1,
            (objPose[0] + adder * 0.001, objPose[1] + adder * 0.001, objPose[2] + adder * 0.001),
            client.simxServiceCall()
        )
        # print("hexa_base: ", objPose[2])

        if legPos == None:
            __e, legPos = client.simxGetObjectPosition(targetLegHand, -1, client.simxServiceCall())

        print(f"leg x {legPos[0]}    leg y {legPos[1]}   leg z {legPos[2]}")
        __e = client.simxSetObjectPosition(targetLegHand, "sim.handle_parent",
                                           (0.2 + 0.07 * sin(adder * 0.02), 0.0 + 0.03 * cos(adder * 0.02), 0),
                                           client.simxServiceCall())

        # client.simxSetObjectPosition(objHand,-1, (10, 5, 0), client.simxServiceCall())
        # if objPose[2]<0.01:
        #    flag=False

        doNextStep = True


    client.simxSynchronous(True)
    client.simxGetSimulationStepDone(client.simxDefaultSubscriber(simulationStepDone));

    errHand, objHand = client.simxGetObjectHandle('Cuboid', client.simxServiceCall())
    errHand, targetLegHand = client.simxGetObjectHandle('hexa_footTarget0', client.simxServiceCall())

    client.simxStartSimulation(client.simxDefaultPublisher())

    startTime = time.time()
    # while time.time()<startTime+5:

    while flag:
        if doNextStep:
            doNextStep = False
            client.simxSynchronousTrigger()
        client.simxSpinOnce()
    print("Stop simulation.")
    client.simxStopSimulation(client.simxDefaultPublisher())