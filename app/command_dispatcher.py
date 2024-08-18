from handlers import handle_help, handle_hi, handle_admin, handle_rcon_command, create_command_handler

def get_command_mapping(help_embeds, command_handler):
    return {
        'help': lambda message, args, auth_level: handle_help(message, args, help_embeds),
        'hi':  lambda message, args, auth_level: handle_hi(message, args),
        'admin': lambda message, args, auth_level: handle_admin(message, args, auth_level, command_handler),
    }

def dispatch_command(cmd, message, args, auth_level, cmds, help_embeds, command_handler):
    command_mapping = get_command_mapping(help_embeds, command_handler)
    
    if cmd in command_mapping:
        return command_mapping[cmd](message, args, auth_level)
    elif cmd in cmds['user_commands']:
        return handle_rcon_command(message, cmd, args, auth_level, required_level=1, command_handler=command_handler)
    elif cmd in cmds['mod_commands']:
        return handle_rcon_command(message, cmd, args, auth_level, required_level=2, command_handler=command_handler)
    elif cmd in cmds['admin_commands']:
        return handle_rcon_command(message, cmd, args, auth_level, required_level=4, command_handler=command_handler)
    else:
        return message.channel.send('Invalid command.')
