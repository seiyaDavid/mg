for name, group in grouped_dfs.items():
    # Sanitize the name to be safe for filenames
    safe_name = str(name).replace(" ", "_").replace("/", "_")
    group.to_csv(f"{safe_name}.csv", index=False)
