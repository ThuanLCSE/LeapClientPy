import redis
import time
import traceback
import json

json_string = '{"sensors":[{"dump":"Frame Info:<br/>Frame [ id:61050 | timestamp:199353550559 | Hand count:(1) | Pointable count:(5) | Gesture count:(0) ]<br/><br/>Hands:<br/>  Hand (right) [ id: 32 | palm velocity:0,0,0 | sphere center:undefined ] <br/><br/><br/>Pointables:<br/>  Finger [ id:320 46.958832mmx | width:18.731209mm | direction:0.522406,0.155241,-0.838447 ]<br/>  Finger [ id:321 48.697384mmx | width:17.89205mm | direction:0.721105,-0.344542,-0.601081 ]<br/>  Finger [ id:322 52.26046mmx | width:17.572371mm | direction:0.603717,-0.123691,-0.787544 ]<br/>  Finger [ id:323 49.583923mmx | width:16.721226mm | direction:0.626101,-0.116524,-0.770986 ]<br/>  Finger [ id:324 44.753723mmx | width:14.8531mm | direction:0.013646,-0.74178,-0.670504 ]<br/><br/><br/>Gestures:<br/><br/><br/>Raw JSON:<br/>{\\"currentFrameRate\\":30.032488,\\"devices\\":[],\\"hands\\":[{\\"armBasis\\":[[0.764928,0.094654,0.637123],[-0.340464,0.899087,0.275186],[-0.546781,-0.427415,0.719963]],\\"armWidth\\":58.940872,\\"confidence\\":1,\\"direction\\":[0.628451,0.564875,-0.534756],\\"elbow\\":[-90.4589,36.892487,269.818481],\\"grabAngle\\":1.282147,\\"grabStrength\\":0,\\"id\\":32,\\"palmNormal\\":[0.437424,-0.825125,-0.357532],\\"palmPosition\\":[86.532654,178.480316,43.840359],\\"palmVelocity\\":[0,0,0],\\"palmWidth\\":84.165565,\\"pinchDistance\\":39.936417,\\"pinchStrength\\":0.438348,\\"timeVisible\\":0,\\"type\\":\\"right\\",\\"wrist\\":[46.099457,143.639084,90.008125]}],\\"id\\":61050,\\"pointables\\":[{\\"bases\\":[[[-0.00979,0.851951,0.52353],[-0.95853,0.141133,-0.247593],[-0.284825,-0.504243,0.815238]],[[0.09776,0.955758,0.277433],[-0.887161,0.210018,-0.410899],[-0.450986,-0.205958,0.868443]],[[0.113938,0.961761,0.249064],[-0.845051,0.225644,-0.484742],[-0.522406,-0.155241,0.838447]],[[0.113871,0.961741,0.249172],[-0.845227,0.225591,-0.484458],[-0.522134,-0.155442,0.838578]]],\\"btipPosition\\":[92.870705,164.120911,-21.115459],\\"carpPosition\\":[47.73513,147.416199,57.943844],\\"dipPosition\\":[84.429901,161.608047,-7.55903],\\"direction\\":[0.522406,0.155241,-0.838447],\\"extended\\":false,\\"handId\\":32,\\"id\\":320,\\"length\\":46.958832,\\"mcpPosition\\":[47.73513,147.416199,57.943844],\\"pipPosition\\":[68.343536,156.827728,18.259144],\\"timeVisible\\":0,\\"tipPosition\\":[92.870705,164.120911,-21.115459],\\"type\\":0,\\"width\\":18.731209},{\\"bases\\":[[[0.739589,0.103937,0.664985],[-0.356704,0.89837,0.256307],[-0.570763,-0.426765,0.701499]],[[0.756556,0.111861,0.64429],[-0.172104,0.984586,0.03115],[-0.630875,-0.134451,0.764147]],[[0.669886,0.125329,0.73181],[0.176806,0.930367,-0.321179],[-0.721105,0.344542,0.601081]],[[0.648601,0.137618,0.748584],[0.286506,0.867035,-0.407633],[-0.705147,0.478865,0.522931]]],\\"btipPosition\\":[128.404221,187.255875,-29.889116],\\"carpPosition\\":[44.669056,165.119965,63.355194],\\"dipPosition\\":[120.98774,192.292404,-24.389112],\\"direction\\":[0.721105,-0.344542,-0.601081],\\"extended\\":true,\\"handId\\":32,\\"id\\":321,\\"length\\":48.697384,\\"mcpPosition\\":[83.510483,194.162033,15.616947],\\"pipPosition\\":[106.721542,199.108749,-12.497436],\\"timeVisible\\":0,\\"tipPosition\\":[128.404221,187.255875,-29.889116],\\"type\\":1,\\"width\\":17.89205},{\\"bases\\":[[[0.705577,-0.10936,0.700144],[-0.238976,0.893421,0.38038],[-0.667121,-0.435705,0.604243]],[[0.687765,-0.118212,0.716244],[-0.104487,0.960258,0.258818],[-0.718375,-0.252844,0.64808]],[[0.780546,-0.109148,0.615495],[0.16209,0.9863,-0.030652],[-0.603717,0.123691,0.787544]],[[0.780546,-0.109148,0.615495],[0.16209,0.9863,-0.030651],[-0.603717,0.123691,0.787545]]],\\"btipPosition\\":[144.204453,199.493469,-19.804985],\\"carpPosition\\":[53.313358,165.533432,70.292068],\\"dipPosition\\":[137.795044,200.806641,-11.443956],\\"direction\\":[0.603717,-0.123691,-0.787544],\\"extended\\":true,\\"handId\\":32,\\"id\\":322,\\"length\\":52.26046,\\"mcpPosition\\":[96.366211,193.651794,31.297071],\\"pipPosition\\":[124.457993,203.539169,5.95413],\\"timeVisible\\":0,\\"tipPosition\\":[144.204453,199.493469,-19.804985],\\"type\\":2,\\"width\\":17.572371},{\\"bases\\":[[[0.615708,-0.239322,0.750752],[-0.2091,0.86898,0.448498],[-0.759724,-0.433126,0.484996]],[[0.622532,-0.236469,0.746014],[-0.019412,0.948298,0.316787],[-0.782354,-0.211691,0.585755]],[[0.738517,-0.228632,0.634288],[0.250182,0.966514,0.057092],[-0.626101,0.116524,0.770986]],[[0.730574,-0.227377,0.643864],[0.227122,0.970159,0.084897],[-0.643954,0.084212,0.760415]]],\\"btipPosition\\":[154.030579,193.645447,3.769296],\\"carpPosition\\":[61.908588,164.281754,77.185699],\\"dipPosition\\":[147.213028,194.537003,11.819818],\\"direction\\":[0.626101,-0.116524,-0.770986],\\"extended\\":true,\\"handId\\":32,\\"id\\":323,\\"length\\":49.583923,\\"mcpPosition\\":[105.928413,189.377899,49.08411],\\"pipPosition\\":[134.049286,196.986908,28.029766],\\"timeVisible\\":0,\\"tipPosition\\":[154.030579,193.645447,3.769296],\\"type\\":3,\\"width\\":16.721226},{\\"bases\\":[[[0.549669,-0.428112,0.717345],[-0.177082,0.779476,0.600882],[-0.816398,-0.457316,0.352643]],[[0.696156,-0.370187,0.615085],[0.173737,0.918201,0.35598],[-0.696551,-0.140955,0.703526]],[[0.762353,-0.42619,0.487011],[0.647017,0.517807,-0.559683],[-0.013646,0.74178,0.670504]],[[0.675506,-0.598126,0.431203],[0.154741,-0.456782,-0.876017],[0.720935,0.65848,-0.216005]]],\\"btipPosition\\":[129.247467,167.432617,35.806343],\\"carpPosition\\":[72.00338,159.12471,85.731331],\\"dipPosition\\":[137.787796,175.233093,33.247509],\\"direction\\":[0.013646,-0.74178,-0.670504],\\"extended\\":false,\\"handId\\":32,\\"id\\":324,\\"length\\":44.753723,\\"mcpPosition\\":[115.791855,183.653381,66.816902],\\"pipPosition\\":[137.55188,188.056763,44.838974],\\"timeVisible\\":0,\\"tipPosition\\":[129.247467,167.432617,35.806343],\\"type\\":4,\\"width\\":14.8531}],\\"timestamp\\":199353550559}","toString":"Frame [ id:61050 | timestamp:199353550559 | Hand count:(1) | Pointable count:(5) | Gesture count:(0) ]","hands":[{"palmPosition":[86.532654,178.480316,43.840359],"grabStrength":0,"confidence":1,"direction":[0.628451,0.564875,-0.534756],"palmNormal":[0.437424,-0.825125,-0.357532],"palmVelocity":[0,0,0],"pinchStrength":0.438348,"type":"right","toString":"Hand (right) [ id: 32 | palm velocity:0,0,0 | sphere center:undefined ] ","roll":0.4874605228409559,"pitch":0.8127814141930815,"yaw":0.8657734967809972,"arm":{"basis":[[0.764928,0.094654,0.637123],[-0.340464,0.899087,0.275186],[-0.546781,-0.427415,0.719963]],"width":58.940872,"center":[-22.17972183227539,90.26578521728516,179.91329956054688],"matrix":[0.7649279832839966,0.09465400129556656,0.6371229887008667,-22.17972183227539,-0.3404639959335327,0.8990870118141174,0.2751860022544861,90.26578521728516,-0.5467810034751892,-0.42741501331329346,0.719963014125824,179.91329956054688,0,0,0,1],"nextJoint":[46.099457,143.639084,90.008125],"prevJoint":[-90.4589,36.892487,269.818481],"type":4},"fingers":[{"bones":[{"basis":[[-0.00979,0.851951,0.52353],[-0.95853,0.141133,-0.247593],[-0.284825,-0.504243,0.815238]],"center":[47.735130310058594,147.41619873046875,57.943843841552734],"matrix":[-0.009789999574422836,0.851951003074646,0.5235300064086914,47.735130310058594,-0.9585300087928772,0.14113299548625946,-0.2475930005311966,147.41619873046875,-0.28482499718666077,-0.504243016242981,0.8152379989624023,57.943843841552734,0,0,0,1],"nextJoint":[47.73513,147.416199,57.943844],"prevJoint":[47.73513,147.416199,57.943844],"width":18.731209,"type":0},{"basis":[[0.09776,0.955758,0.277433],[-0.887161,0.210018,-0.410899],[-0.450986,-0.205958,0.868443]],"center":[58.03933334350586,152.12196350097656,38.10149383544922],"matrix":[0.09775999933481216,0.9557579755783081,0.27743300795555115,58.03933334350586,-0.8871610164642334,0.21001799404621124,-0.41089901328086853,152.12196350097656,-0.45098599791526794,-0.20595799386501312,0.8684430122375488,38.10149383544922,0,0,0,1],"nextJoint":[68.343536,156.827728,18.259144],"prevJoint":[47.73513,147.416199,57.943844],"width":18.731209,"type":1},{"basis":[[0.113938,0.961761,0.249064],[-0.845051,0.225644,-0.484742],[-0.522406,-0.155241,0.838447]],"center":[76.38671875,159.21788024902344,5.350057125091553],"matrix":[0.11393799632787704,0.9617609977722168,0.24906399846076965,76.38671875,-0.8450509905815125,0.22564400732517242,-0.4847419857978821,159.21788024902344,-0.5224059820175171,-0.155240997672081,0.8384469747543335,5.350057125091553,0,0,0,1],"nextJoint":[84.429901,161.608047,-7.55903],"prevJoint":[68.343536,156.827728,18.259144],"width":18.731209,"type":2},{"basis":[[0.113871,0.961741,0.249172],[-0.845227,0.225591,-0.484458],[-0.522134,-0.155442,0.838578]],"center":[88.65030670166016,162.86447143554688,-14.337244033813477],"matrix":[0.1138710007071495,0.9617409706115723,0.24917200207710266,88.65030670166016,-0.8452270030975342,0.2255910038948059,-0.48445799946784973,162.86447143554688,-0.522134006023407,-0.1554419994354248,0.8385779857635498,-14.337244033813477,0,0,0,1],"nextJoint":[92.870705,164.120911,-21.115459],"prevJoint":[84.429901,161.608047,-7.55903],"width":18.731209,"type":3}],"type":0,"extended":false,"toString":"Finger [ id:320 46.958832mmx | width:18.731209mm | direction:0.522406,0.155241,-0.838447 ]","carpPosition":[47.73513,147.416199,57.943844],"dipPosition":[84.429901,161.608047,-7.55903],"mcpPosition":[47.73513,147.416199,57.943844],"pipPosition":[68.343536,156.827728,18.259144],"tipPosition":[92.870705,164.120911,-21.115459],"length":46.958832,"timeVisible":0,"width":18.731209},{"bones":[{"basis":[[0.739589,0.103937,0.664985],[-0.356704,0.89837,0.256307],[-0.570763,-0.426765,0.701499]],"center":[64.08976745605469,179.64100646972656,39.48606872558594],"matrix":[0.7395889759063721,0.10393700003623962,0.6649850010871887,64.08976745605469,-0.3567039966583252,0.8983700275421143,0.2563070058822632,179.64100646972656,-0.5707629919052124,-0.42676499485969543,0.7014989852905273,39.48606872558594,0,0,0,1],"nextJoint":[83.510483,194.162033,15.616947],"prevJoint":[44.669056,165.119965,63.355194],"width":17.89205,"type":0},{"basis":[[0.756556,0.111861,0.64429],[-0.172104,0.984586,0.03115],[-0.630875,-0.134451,0.764147]],"center":[95.11601257324219,196.63539123535156,1.5597554445266724],"matrix":[0.75655597448349,0.11186099797487259,0.6442899703979492,95.11601257324219,-0.17210400104522705,0.9845860004425049,0.031150000169873238,196.63539123535156,-0.6308749914169312,-0.1344510018825531,0.7641469836235046,1.5597554445266724,0,0,0,1],"nextJoint":[106.721542,199.108749,-12.497436],"prevJoint":[83.510483,194.162033,15.616947],"width":17.89205,"type":1},{"basis":[[0.669886,0.125329,0.73181],[0.176806,0.930367,-0.321179],[-0.721105,0.344542,0.601081]],"center":[113.85464477539062,195.70057678222656,-18.443273544311523],"matrix":[0.6698859930038452,0.12532900273799896,0.7318099737167358,113.85464477539062,0.1768060028553009,0.9303669929504395,-0.32117900252342224,195.70057678222656,-0.7211049795150757,0.344541996717453,0.6010810136795044,-18.443273544311523,0,0,0,1],"nextJoint":[120.98774,192.292404,-24.389112],"prevJoint":[106.721542,199.108749,-12.497436],"width":17.89205,"type":2},{"basis":[[0.648601,0.137618,0.748584],[0.286506,0.867035,-0.407633],[-0.705147,0.478865,0.522931]],"center":[124.69598388671875,189.77413940429688,-27.139114379882812],"matrix":[0.6486009955406189,0.13761800527572632,0.748583972454071,124.69598388671875,0.2865059971809387,0.8670349717140198,-0.4076330065727234,189.77413940429688,-0.7051470279693604,0.47886499762535095,0.5229309797286987,-27.139114379882812,0,0,0,1],"nextJoint":[128.404221,187.255875,-29.889116],"prevJoint":[120.98774,192.292404,-24.389112],"width":17.89205,"type":3}],"type":1,"extended":true,"toString":"Finger [ id:321 48.697384mmx | width:17.89205mm | direction:0.721105,-0.344542,-0.601081 ]","carpPosition":[44.669056,165.119965,63.355194],"dipPosition":[120.98774,192.292404,-24.389112],"mcpPosition":[83.510483,194.162033,15.616947],"pipPosition":[106.721542,199.108749,-12.497436],"tipPosition":[128.404221,187.255875,-29.889116],"length":48.697384,"timeVisible":0,"width":17.89205},{"bones":[{"basis":[[0.705577,-0.10936,0.700144],[-0.238976,0.893421,0.38038],[-0.667121,-0.435705,0.604243]],"center":[74.83978271484375,179.5926055908203,50.79457092285156],"matrix":[0.70557701587677,-0.10936000198125839,0.7001439929008484,74.83978271484375,-0.23897600173950195,0.8934209942817688,0.3803800046443939,179.5926055908203,-0.6671209931373596,-0.4357050061225891,0.6042429804801941,50.79457092285156,0,0,0,1],"nextJoint":[96.366211,193.651794,31.297071],"prevJoint":[53.313358,165.533432,70.292068],"width":17.572371,"type":0},{"basis":[[0.687765,-0.118212,0.716244],[-0.104487,0.960258,0.258818],[-0.718375,-0.252844,0.64808]],"center":[110.41210174560547,198.59547424316406,18.625600814819336],"matrix":[0.6877650022506714,-0.11821199953556061,0.7162439823150635,110.41210174560547,-0.10448700189590454,0.9602580070495605,0.25881800055503845,198.59547424316406,-0.718375027179718,-0.2528440058231354,0.6480799913406372,18.625600814819336,0,0,0,1],"nextJoint":[124.457993,203.539169,5.95413],"prevJoint":[96.366211,193.651794,31.297071],"width":17.572371,"type":1},{"basis":[[0.780546,-0.109148,0.615495],[0.16209,0.9863,-0.030652],[-0.603717,0.123691,0.787544]],"center":[131.12652587890625,202.17291259765625,-2.744913101196289],"matrix":[0.7805460095405579,-0.10914800316095352,0.6154950261116028,131.12652587890625,0.162090003490448,0.986299991607666,-0.03065199963748455,202.17291259765625,-0.603717029094696,0.12369100004434586,0.7875440120697021,-2.744913101196289,0,0,0,1],"nextJoint":[137.795044,200.806641,-11.443956],"prevJoint":[124.457993,203.539169,5.95413],"width":17.572371,"type":2},{"basis":[[0.780546,-0.109148,0.615495],[0.16209,0.9863,-0.030651],[-0.603717,0.123691,0.787545]],"center":[140.999755859375,200.15005493164062,-15.624470710754395],"matrix":[0.7805460095405579,-0.10914800316095352,0.6154950261116028,140.999755859375,0.162090003490448,0.986299991607666,-0.030650999397039413,200.15005493164062,-0.603717029094696,0.12369100004434586,0.7875450253486633,-15.624470710754395,0,0,0,1],"nextJoint":[144.204453,199.493469,-19.804985],"prevJoint":[137.795044,200.806641,-11.443956],"width":17.572371,"type":3}],"type":2,"extended":true,"toString":"Finger [ id:322 52.26046mmx | width:17.572371mm | direction:0.603717,-0.123691,-0.787544 ]","carpPosition":[53.313358,165.533432,70.292068],"dipPosition":[137.795044,200.806641,-11.443956],"mcpPosition":[96.366211,193.651794,31.297071],"pipPosition":[124.457993,203.539169,5.95413],"tipPosition":[144.204453,199.493469,-19.804985],"length":52.26046,"timeVisible":0,"width":17.572371},{"bones":[{"basis":[[0.615708,-0.239322,0.750752],[-0.2091,0.86898,0.448498],[-0.759724,-0.433126,0.484996]],"center":[83.91850280761719,176.829833984375,63.13490295410156],"matrix":[0.6157079935073853,-0.2393220067024231,0.7507519721984863,83.91850280761719,-0.20909999310970306,0.8689799904823303,0.448498010635376,176.829833984375,-0.7597240209579468,-0.4331260025501251,0.4849959909915924,63.13490295410156,0,0,0,1],"nextJoint":[105.928413,189.377899,49.08411],"prevJoint":[61.908588,164.281754,77.185699],"width":16.721226,"type":0},{"basis":[[0.622532,-0.236469,0.746014],[-0.019412,0.948298,0.316787],[-0.782354,-0.211691,0.585755]],"center":[119.98884582519531,193.18240356445312,38.55693817138672],"matrix":[0.6225320100784302,-0.23646900057792664,0.7460139989852905,119.98884582519531,-0.019411999732255936,0.9482979774475098,0.3167870044708252,193.18240356445312,-0.7823539972305298,-0.2116910070180893,0.5857549905776978,38.55693817138672,0,0,0,1],"nextJoint":[134.049286,196.986908,28.029766],"prevJoint":[105.928413,189.377899,49.08411],"width":16.721226,"type":1},{"basis":[[0.738517,-0.228632,0.634288],[0.250182,0.966514,0.057092],[-0.626101,0.116524,0.770986]],"center":[140.63116455078125,195.761962890625,19.92479133605957],"matrix":[0.7385169863700867,-0.22863200306892395,0.6342880129814148,140.63116455078125,0.25018200278282166,0.966513991355896,0.05709199979901314,195.761962890625,-0.626101016998291,0.11652400344610214,0.770986020565033,19.92479133605957,0,0,0,1],"nextJoint":[147.213028,194.537003,11.819818],"prevJoint":[134.049286,196.986908,28.029766],"width":16.721226,"type":2},{"basis":[[0.730574,-0.227377,0.643864],[0.227122,0.970159,0.084897],[-0.643954,0.084212,0.760415]],"center":[150.62181091308594,194.0912322998047,7.794557094573975],"matrix":[0.7305740118026733,-0.2273769974708557,0.6438639760017395,150.62181091308594,0.2271219938993454,0.9701589941978455,0.0848969966173172,194.0912322998047,-0.6439539790153503,0.08421199768781662,0.7604150176048279,7.794557094573975,0,0,0,1],"nextJoint":[154.030579,193.645447,3.769296],"prevJoint":[147.213028,194.537003,11.819818],"width":16.721226,"type":3}],"type":3,"extended":true,"toString":"Finger [ id:323 49.583923mmx | width:16.721226mm | direction:0.626101,-0.116524,-0.770986 ]","carpPosition":[61.908588,164.281754,77.185699],"dipPosition":[147.213028,194.537003,11.819818],"mcpPosition":[105.928413,189.377899,49.08411],"pipPosition":[134.049286,196.986908,28.029766],"tipPosition":[154.030579,193.645447,3.769296],"length":49.583923,"timeVisible":0,"width":16.721226},{"bones":[{"basis":[[0.549669,-0.428112,0.717345],[-0.177082,0.779476,0.600882],[-0.816398,-0.457316,0.352643]],"center":[93.89762115478516,171.3890380859375,76.27411651611328],"matrix":[0.5496690273284912,-0.4281120002269745,0.7173449993133545,93.89762115478516,-0.17708200216293335,0.77947598695755,0.6008819937705994,171.3890380859375,-0.816398024559021,-0.45731601119041443,0.3526430130004883,76.27411651611328,0,0,0,1],"nextJoint":[115.791855,183.653381,66.816902],"prevJoint":[72.00338,159.12471,85.731331],"width":14.8531,"type":0},{"basis":[[0.696156,-0.370187,0.615085],[0.173737,0.918201,0.35598],[-0.696551,-0.140955,0.703526]],"center":[126.67186737060547,185.85507202148438,55.827938079833984],"matrix":[0.6961560249328613,-0.37018701434135437,0.6150850057601929,126.67186737060547,0.17373700439929962,0.9182010293006897,0.3559800088405609,185.85507202148438,-0.6965510249137878,-0.14095500111579895,0.7035260200500488,55.827938079833984,0,0,0,1],"nextJoint":[137.55188,188.056763,44.838974],"prevJoint":[115.791855,183.653381,66.816902],"width":14.8531,"type":1},{"basis":[[0.762353,-0.42619,0.487011],[0.647017,0.517807,-0.559683],[-0.013646,0.74178,0.670504]],"center":[137.6698455810547,181.64492797851562,39.04323959350586],"matrix":[0.7623530030250549,-0.42618998885154724,0.48701098561286926,137.6698455810547,0.6470170021057129,0.5178070068359375,-0.5596830248832703,181.64492797851562,-0.013646000064909458,0.7417799830436707,0.6705039739608765,39.04323959350586,0,0,0,1],"nextJoint":[137.787796,175.233093,33.247509],"prevJoint":[137.55188,188.056763,44.838974],"width":14.8531,"type":2},{"basis":[[0.675506,-0.598126,0.431203],[0.154741,-0.456782,-0.876017],[0.720935,0.65848,-0.216005]],"center":[133.5176239013672,171.33285522460938,34.52692413330078],"matrix":[0.6755059957504272,-0.5981259942054749,0.4312030076980591,133.5176239013672,0.15474100410938263,-0.4567820131778717,-0.8760169744491577,171.33285522460938,0.7209349870681763,0.6584799885749817,-0.21600499749183655,34.52692413330078,0,0,0,1],"nextJoint":[129.247467,167.432617,35.806343],"prevJoint":[137.787796,175.233093,33.247509],"width":14.8531,"type":3}],"type":4,"extended":false,"toString":"Finger [ id:324 44.753723mmx | width:14.8531mm | direction:0.013646,-0.74178,-0.670504 ]","carpPosition":[72.00338,159.12471,85.731331],"dipPosition":[137.787796,175.233093,33.247509],"mcpPosition":[115.791855,183.653381,66.816902],"pipPosition":[137.55188,188.056763,44.838974],"tipPosition":[129.247467,167.432617,35.806343],"length":44.753723,"timeVisible":0,"width":14.8531}]}],"id":61050,"positionX":0,"positionY":0}]}'
def RedisCheck():
    try:
        r = redis.StrictRedis(host='localhost', port=6379)                         

        p = r.pubsub()                                                              
        p.subscribe('leapthuan')                                                 
        PAUSE = True

        while PAUSE:                                                                
            print("Waiting For aaa...")
            message = p.get_message()
            if message:
                command = message['data']                                           

                if command == b'top':                                             
                    PAUSE = False
                else:
                    print("mess: ",command)

            time.sleep(1)

        print("Permission to start...")

    except Exception as e:
        print("!!!!!!!!!! EXCEPTION !!!!!!!!!")
        print(str(e))
        print(traceback.format_exc())
 
#RedisCheck()

datastore = json.loads(json_string)

print(datastore['sensors'][0]['hands'][0]['toString'])
print(datastore['sensors'][0]['hands'][1]['toString'])
class Payload(object):
    def __init__(self, action, method, data):
        self.action = action
        self.method = method
        self.data = data

import json

def as_payload(dct):
    return Payload(dct['action'], dct['method'], dct['data'])

j = '{"action": "print", "method": "onData", "data": ["Madan Mohan","hehehe","jaja"]}'
p = json.loads(j, object_hook = as_payload)
g = json.loads('[{"action": "print", "method": "onData"},{"action": "print", "method": "onData"}]')
