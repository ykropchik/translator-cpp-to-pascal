int    number(int b) {
    return b;
}

int main() {
    int a = number(4);
    int b = a;
    int c = a + b;
    int d;
    if(c <= a) {
        d = a;
    } else {
        d = c;
    }
}