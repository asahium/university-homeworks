void div_by_minus_four(float* arg) {
    unsigned int *x = (float*)(arg)
    
    *x -= (1u << 24);
    *x ^= (1u << 31);
}
