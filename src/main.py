 
from file_io import import_full_electoral_role, import_electoral_role_update
from conversion import monthly_update_to_full_file, full_file_to_tvv_upload
from crud import apply_create, apply_deletes, apply_edits

def main() -> None:
    print("Starting electoral role file converter...")

    main_file = input("Please provide the path to the main electoral role: ")
    main_file_data = import_full_electoral_role(main_file)

    update_file = input("Please provide the path to the monthly update file: ")
    data_creates, data_edits, data_deletes = import_electoral_role_update(update_file)

    print("Finding updates...")
    data_creates = monthly_update_to_full_file(data_creates)
    data_edits = monthly_update_to_full_file(data_edits)
    data_deletes = monthly_update_to_full_file(data_deletes)

    print("Applying updates...")
    main_file_data = apply_deletes(main_file_data, data_deletes)
    main_file_data = apply_create(main_file_data, data_creates)
    main_file_data = apply_edits(main_file_data, data_edits)

    print("Saving...")
    main_file_data.to_csv("merged_electoral_role.csv", index=False, encoding="utf-8-sig")

    import_tvv = input("Convert to TVV format (y/n): ")
    if import_tvv.lower() == "y":
        print("Converting to TVV format...")
        tvv_file = full_file_to_tvv_upload(main_file_data)

        # split files over 100k lines into multiple output files
        if tvv_file.shape[0] > 100000:
            for i in range(0, tvv_file.shape[0], 100000):
                tvv_file[i:i+100000].to_csv(f"tvv_upload_{i}.csv", index=False, encoding="utf-8-sig")
        else:       
            tvv_file.to_csv("tvv_upload.csv", index=False, encoding="utf-8-sig")

    print("Done!")



if __name__ == "__main__": 
    main()