import sys; sys.path.insert(0, '/Users/sumit/Github/corner_function/scripts'); import sigma3d as S3
S = S3.Strip3D(10, 8, 8, list(range(4, 6)), 3); S3.route_i_ckpt(S, '/Users/sumit/Github/corner_function/scripts/ckB.json', cpts=12, with_saddle=True)
