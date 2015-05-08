#!/usr/bin/env python
{imports}

def main():
    import argparse
    parser = argparse.ArgumentParser()
{args}
    args = parser.parse_args()

if __name__ == '__main__':
    main()
