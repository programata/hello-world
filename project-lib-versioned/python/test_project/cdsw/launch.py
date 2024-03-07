import os
import sys
import subprocess


def main():
    # Fijar el directorio de trabajo en el raíz del proyecto Kedro.
    os.chdir('/home/cdsw/code/src/test/test_project')

    # Indicar el valor fechadato que corresponda
    fechadato = '20219999'
    cp = subprocess.run(['/home/cdsw/shell/launch.sh', fechadato], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('\n=========STDERR========\n', cp.stderr)

    print('\n=========STDOUT========\n', cp.stdout)

    if cp.returncode != 0:
        sys.exit(cp.stderr)


if __name__ == "__main__":
    main()
