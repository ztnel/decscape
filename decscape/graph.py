
import matplotlib.pyplot as plt # type:ignore

def filter_zero(categories:list[str], values:list[int]) -> tuple[list[str], list[int]]:
    # Plot data on each subplots
    cat_names = []
    filt_values = []
    for idx,name in enumerate(categories):
        if values[idx] != 0:
            cat_names.append(name)
    filt_values = list(filter(lambda x: x != 0, values))
    return (cat_names, filt_values)

def plot(categories: list[str], values:list[int], title:str, xlabel: str, ylabel:str) -> None:
    filt_categories, filt_values = filter_zero(categories, values)
    plt.figure()
    plt.barh(filt_categories, filt_values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
def show() -> None:
    plt.show()
