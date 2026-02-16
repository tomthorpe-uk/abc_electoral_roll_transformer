 
from dataclasses import dataclass

from src.file_io import import_full_electoral_role, import_electoral_role_update

def main() -> None:
    full_path = r"/home/tom-thorpe/code/abc_electoral_role_transformer/data/dec_2025_fuil.csv"
    data_full = pd.read_csv(full_path)

    update_path = r"/home/tom-thorpe/code/abc_electoral_role_transformer/data/dec_2025_fuil.csv"
    data_update = pd.read_csv(full_path)


if __name__ == "__main__": 
    main()