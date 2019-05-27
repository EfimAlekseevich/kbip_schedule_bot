import json

emodji11 ='😀😃😄😁😆😅😂🤣☺️😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽'
good_emodji = '😊☺️😚😙😗😛😝😋😜🎶🤪🎶'
emodji1 = []
emodji2 = []
for emodj in emodji11:
    emodji1.append(emodj)

for emodj in good_emodji:
    emodji2.append(emodj)

emodji = {
    'all_emodji': emodji1,
    'good_emodji': emodji2
}

f = open('emodji.json', 'w')
json.dump(emodji, f)
f.close()