from auth import _generate_uuid

def test_generate_uuid():
    uuid_str = _generate_uuid()
    print("Generated UUID:", uuid_str)

if __name__ == "__main__":
    test_generate_uuid()


