class City(str):
    def __hash__(self):
        return ord(self[0])


if __name__ == "__main__":
    print(
        "Adding Rome, San Francisco, New York and Barcelona to a set.  New York and Barcenlona will collide!"
    )
    # We create a dictionary where we assign arbitrary values to cities
    data = {
        City("Rome"): "Italy",
        City("San Francisco"): "USA",
        City("New York"): "USA",
        City("Barcelona"): "Spain",
    }
