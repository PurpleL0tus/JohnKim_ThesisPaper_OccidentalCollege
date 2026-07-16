import scipy.stats as stats


def normal_distribution(mean, std_dev, lower_bound=0, upper_bound=10):
    while True:
        val = stats.norm.rvs(loc=mean, scale=std_dev)
        if lower_bound <= val <= upper_bound:
            return round(val)


if __name__ == '__main__':
    result = normal_distribution(3, 1)
    print(f"result: {result}")
