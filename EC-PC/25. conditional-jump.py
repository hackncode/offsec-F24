import pwn
pwn.context.update(arch="amd64")
code = pwn.asm("""
mov ebx, [rdi+4]          # Load the signed dword value from memory address [rdi+4] into ebx
mov ecx, [rdi+8]          # Load the signed dword value from memory address [rdi+8] into ecx
mov edx, [rdi+12]         # Load the signed dword value from memory address [rdi+12] into edx
mov eax, [rdi]            # Load the signed dword value from memory address [rdi] into eax
cmp eax, 0x7f454c46       # Compare eax with 0x7f454c46 (magic number 1)
je down1                  # If equal, jump to the 'down1' label
mov eax, [rdi]            # Reload the value at [rdi] into eax
cmp eax, 0x00005A4D       # Compare eax with 0x00005A4D (magic number 2)
je down2                  # If equal, jump to the 'down2' label
imul ebx, ecx             # Default case: Multiply ebx by ecx
imul ebx, edx             # Multiply the result by edx
jmp done                  # Jump to the 'done' label
nop                       # No-operation padding (not strictly necessary)
down1:                    # Case for when [rdi] == 0x7f454c46
add ebx, ecx              # Add ecx to ebx
add ebx, edx              # Add edx to the result in ebx
jmp done                  # Jump to the 'done' label
down2:                    # Case for when [rdi] == 0x00005A4D
sub ebx, ecx              # Subtract ecx from ebx
sub ebx, edx              # Subtract edx from the result in ebx
done:                     # Final label
mov eax, ebx              # Move the result from ebx to eax (output result)
""")
process = pwn.process("/challenge/run")
process.write(code)
print(process.readall())