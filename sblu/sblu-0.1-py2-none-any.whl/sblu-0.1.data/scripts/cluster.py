#!python
import numpy as np


def cluster(pwrmsds, cluster_radius, min_clust_size, max_clusters):
    marked = set()

    cluster_indices = [set(np.where(row <= cluster_radius)[0]) for
                       row in pwrmsds]
    cluster_centers = list()

    # Find clusters
    for _ in range(max_clusters):
        max_index = None
        max_size = 0

        for j, cluster in enumerate(cluster_indices):
            if j in marked:
                continue

            cluster_size = len(cluster)
            if cluster_size >= min_clust_size and cluster_size > max_size:
                max_index = j
                max_size = cluster_size

        if max_index is None:
            break

        cluster_centers.append(max_index)
        marked.update(cluster_indices[max_index])

    # Reclustering
    final_cluster_assignments = pwrmsds[cluster_centers].argmin(axis=0)
    cluster_members = [[] for _ in range(len(cluster_centers))]

    # Select the members which are a member of at least one cluster
    s2 = set()
    for c in cluster_centers:
        s2 = s2 | cluster_indices[c]

    # Assign those members to the correct cluster
    for i in sorted(s2):
        cluster_members[final_cluster_assignments[i]].append(i)

    return sorted(zip(cluster_centers, cluster_members),
                  key=lambda x: len(x[1]), reverse=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Cluster ftresults")
    parser.add_argument("--radius", "-r", default=9.0, type=float)
    parser.add_argument("--min_cluster_size", "-s", default=10, type=int)
    parser.add_argument("--max_clusters", "-l", default=50, type=int)
    parser.add_argument("--output", "-o", default=None)
    parser.add_argument("--json", default=False)
    parser.add_argument("pwrmsds")

    args = parser.parse_args()

    if args.output is None:
        args.output = "{}.clusters".format(args.pwrmsds)

    pwrmsds = np.loadtxt(args.pwrmsds)
    pwrmsds = pwrmsds.reshape(np.sqrt(len(pwrmsds)), -1)
    assert pwrmsds.shape[0] == pwrmsds.shape[1]

    clusters = cluster(pwrmsds, args.radius,
                       args.min_cluster_size, args.max_clusters)

    if args.output == "--":
        print("Radius\t{:f}".format(args.radius))
        for cluster_center, members in clusters:
            print("Center {}".format(cluster_center+1))
            for member in members:
                print(member+1)
    else:
        with open(args.output, "w") as out:
            out.write("Radius  {:f}\n".format(args.radius))
            for cluster_center, members in clusters:
                out.write("Center {}\n".format(cluster_center+1))
                for member in members:
                    out.write("{}\n".format(member+1))
