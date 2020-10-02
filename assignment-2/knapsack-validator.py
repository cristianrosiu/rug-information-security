# Calculate the gcd of 2 numbers using the euclidean method
def gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    return gcd(b, a % b)


# Checks if a sequence is super-increasing
def is_super(list):
    sum = 0
    for n in list:
        # If current number is smaller or equal to the sum of the previous numbers
        # the sequence can't be called super-increasing
        if n <= sum:
            return False
        sum += n
    return True


# Checks the validity of the given private and public keys.
# Returns -1 ,0 or 1 based on the requirements specified in the assignment paper:
# PRIVATE = WRONG => -1
# PRIVATE = valid & PUBLIC = invalid => 0
# PRIVATE & PUBLIC = valid => 1
# Note: If private key is not valid => public key is not valid
def validate_knapsack(n, m, private, public):
    if sum(private) >= m:
        return -1
    # If n and m are not co-primes, keys are not valid
    if gcd(n, m) != 1:
        return -1
    # If private key sequence is not super-increasing => private key not valid
    if not is_super(private):
        return -1
    else:
        for i in range(len(public)):
            # Check following property: public_key = n * private_key mod (m)
            # This should hold for every key in sequence in order for the public key to be considered valid
            if public[i] != private[i] * n % m:
                return 0

    return 1


# Read the input using the format described in assignment
n, m = [int(x) for x in input().split()]
private_key = [int(x) for x in input().split()]
public_key = [int(x) for x in input().split()]

print(validate_knapsack(n, m, private_key, public_key))
