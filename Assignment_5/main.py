from run import RunScript

if __name__ == "__main__":
    run = RunScript(
        max_number_of_books=1000, 
        max_number_of_authors=500, 
        add_new_entries=False
    )
    run.run()
    