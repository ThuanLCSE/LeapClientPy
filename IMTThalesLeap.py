class Bone:
    def __init__(self, dct):
        self.basis = dct['basis'] if 'basis' in dct else []
        self.center = dct['center'] if 'center' in dct else []
        self.matrix = dct['matrix'] if 'matrix' in dct else []
        self.nextJoint = dct['nextJoint'] if 'nextJoint' in dct else []
        self.prevJoint = dct['prevJoint'] if 'prevJoint' in dct else []
        self.direction = dct['direction'] if 'direction' in dct else []
        self.type = dct['type'] if 'type' in dct else ''
        self.width = dct['width'] if 'width' in dct else ''
        self.length = dct['length'] if 'length' in dct else ''
        
class Pointable:
    def __init__(self, dct):
        self.direction = dct['direction'] if 'direction' in dct else []
        self.stabilizedTipPosition = dct['stabilizedTipPosition'] if 'stabilizedTipPosition' in dct else []
        self.tipPosition = dct['tipPosition'] if 'tipPosition' in dct else []
        self.tipVelocity = dct['tipVelocity'] if 'tipVelocity' in dct else []
        self.length = dct['length'] if 'length' in dct else ''
        self.touchDistance = dct['touchDistance'] if 'touchDistance' in dct else ''
        self.width = dct['width'] if 'width' in dct else ''
        self.value = dct['value'] if 'value' in dct else ''

class Finger:
    def __init__(self, dct): 
        self.bones_dict = dct['bones'] if 'bones' in dct else [] 
        self.carpPosition = dct['carpPosition'] if 'carpPosition' in dct else [] 
        self.dipPosition = dct['dipPosition'] if 'dipPosition' in dct else [] 
        self.mcpPosition = dct['mcpPosition'] if 'mcpPosition' in dct else [] 
        self.pipPosition = dct['pipPosition'] if 'pipPosition' in dct else []
        self.extended = dct['extended'] if 'extended' in dct else ''
        self.type = dct['type'] if 'type' in dct else ''
        self.toString = dct['toString'] if 'toString' in dct else ''
        self.timeVisible = dct['timeVisible'] if 'timeVisible' in dct else ''
        self.direction = dct['direction'] if 'direction' in dct else []
        self.stabilizedTipPosition = dct['stabilizedTipPosition'] if 'stabilizedTipPosition' in dct else []
        self.tipPosition = dct['tipPosition'] if 'tipPosition' in dct else []
        self.tipVelocity = dct['tipVelocity'] if 'tipVelocity' in dct else []
        self.length = dct['length'] if 'length' in dct else ''
        self.touchDistance = dct['touchDistance'] if 'touchDistance' in dct else ''
        self.width = dct['width'] if 'width' in dct else ''
        self.value = dct['value'] if 'value' in dct else ''
    def getBones(self):
        listBone = []
        for b in self.bones_dict:
            listBone.append(Bone(b))
        return listBone 
 
class Hand:
    def __init__(self, dct):
        self.palmPosition = dct['palmPosition'] if 'palmPosition' in dct else []
        self.confidence = dct['confidence'] if 'confidence' in dct else ''
        self.grabStrength = dct['grabStrength'] if 'grabStrength' in dct else ''
        self.direction = dct['direction'] if 'direction' in dct else []
        self.palmNormal = dct['palmNormal'] if 'palmNormal' in dct else []
        self.palmVelocity = dct['palmVelocity'] if 'palmVelocity' in dct else []
        self.palmWidth = dct['palmWidth'] if 'palmWidth' in dct else ''
        self.pinchStrength = dct['pinchStrength'] if 'pinchStrength' in dct else ''
        self.sphereCenter = dct['sphereCenter'] if 'sphereCenter' in dct else []
        self.sphereRadius = dct['sphereRadius = '] if 'sphereRadius = ' in dct else ''
        self.timeVisible = dct['timeVisible'] if 'timeVisible' in dct else ''
        self.stabilizedPalmPosition = dct['stabilizedPalmPosition'] if 'stabilizedPalmPosition' in dct else []
        self.type = dct['type'] if 'type' in dct else ''
        self.arm = dct['arm'] if 'arm' in dct else ''
        self.fingers_dict = dct['fingers'] if 'fingers' in dct else []
        self.pointables =  []
        self.id = dct['id'] if 'id' in dct else ''
        self.roll = dct['roll'] if 'roll' in dct else '' 
        self.pitch = dct['pitch'] if 'pitch' in dct else ''
        self.yaw = dct['yaw'] if 'yaw' in dct else ''
        self.toString = dct['toString'] if 'toString' in dct else ''
        self.reconstructPointable()
    def __str__(self):
        return self.toString
    def getFingers(self):
        listFinger = []
        for finger in self.fingers_dict:
            listFinger.append(Finger(finger))
        return listFinger
    def getPointables(self): 
        return self.pointables
    def reconstructPointable(self):
        for finger in self.fingers_dict:
            self.pointables.append(Pointable(finger)) 
        
class SensorFrame:
    def __init__(self, dct):
        self.dump =  dct['dump'] if 'dump' in dct else ''
        self.toString = dct['toString'] if 'toString' in dct else ''
        self.hands_dict = dct['hands'] if 'hands' in dct else []
        self.positionX = dct['positionX'] if 'positionX' in dct else ''
        self.positionY = dct['positionY'] if 'positionY' in dct else '' 
        self.pointables= []
        self.fingers= []
        self.reconstructPointable()
        
    def reconstructPointable(self):
        for h in self.hands_dict:
            hand = Hand(h)
            self.pointables.extend(hand.getPointables())
            self.fingers.extend(hand.getFingers())
            
    def getPointables(self): 
        return self.pointables
    def getFingers(self): 
        return self.fingers
    def getHands(self):
        listHand = []
        for hand in self.hands_dict:
            listHand.append(Hand(hand))
        return listHand
