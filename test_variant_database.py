import VariantDatabase as vdb



commands = ["x = ca","y = lineages x","save y -"]

for command in commands:
    output = vdb.VariantDatabase().command(command)
    truncatedOutput = (output[:300] + "...") if len(output) > 300 else output
    print("\nOutput from command \""+command+"\":"+truncatedOutput)


    
