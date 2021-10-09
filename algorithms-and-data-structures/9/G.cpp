bool result = false;
int j = size - 1;
for (int i = 0; i < size; i++) {
    if ( (p[i].Y < point.Y && p[j].Y >= point.Y || p[j].Y < point.Y && p[i].Y >= point.Y) &&
         (p[i].X + (point.Y - p[i].Y) / (p[j].Y - p[i].Y) * (p[j].X - p[i].X) < point.X) )
        result = !result;
    j = i;
}
