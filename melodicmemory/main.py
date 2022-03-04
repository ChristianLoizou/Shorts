
if __name__ == "__main__":
    __version__ = "v0.1"

    try:
        from application_update import execute_update
        import os
        if execute_update('melodicmemory', __version__, os.path.basename(__file__)):
            exit()

    except ModuleNotFoundError:
        pass
