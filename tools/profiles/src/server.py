from syml_profiles.service.profiles import SymlProfileService

if __name__ == '__main__':
    service = SymlProfileService()
    service.unix_serve()
