import sys
input = sys.stdin.readline
MOD = 10**9+7

n, k = map(int, input().split())
s = input().strip()

pxX = [0]*(n+1)
pxB = [0]*(n+1)
pxW = [0]*(n+1)

for i in range(n):
    pxX[i+1] = pxX[i] + (s[i] == 'X')
    pxB[i+1] = pxB[i] + (s[i] == 'B')
    pxW[i+1] = pxW[i] + (s[i] == 'W')

def seg_count(px_char, l, r):
    return px_char[r] - px_char[l]

canBlack = [0]*(n+1)
for i in range(n-k+1):
    if seg_count(pxW, i, i+k) == 0:
        canBlack[i] = 1

canWhite = [0]*(n+1)
for i in range(n-k+1):
    if seg_count(pxB, i, i+k) == 0:
        canWhite[i] = 1

total_X = pxX[n]
totalWays = pow(2, total_X, MOD)

X_in_seg = [0]*(n+1)
for i in range(n-k+1):
    X_in_seg[i] = seg_count(pxX, i, i+k)

prefWhite = [0]*(n+2)

for i in range(n-k+1):
    if canWhite[i]:
        w_val = pow(2, total_X - X_in_seg[i], MOD)
        prefWhite[i+1] = (prefWhite[i] + w_val) % MOD
    else:
        prefWhite[i+1] = prefWhite[i]

ans = 0
for b in range(n-k+1):
    if not canBlack[b]:
        continue
    right_sum = prefWhite[n-k+1] - prefWhite[b+1]
    right_sum %= MOD
    val_b = pow(2, total_X - X_in_seg[b], MOD)
    ans = (ans + val_b * right_sum) % MOD

print(ans % MOD)
