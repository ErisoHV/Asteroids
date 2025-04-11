import platform

if platform.system() == 'Windows':
    import simpleguitk as simplegui
else:
    try:
        import simplegui
    except ImportError:
        try:
            import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
        except ImportError:
            raise ImportError("No compatible SimpleGUI module was found. Did you install SimpleGUICS2Pygame?")