
func gen
const

MaxK=100;

type

Square = array [1..MaxK, 1..MaxK] of byte;
{квадрат KxK, повторением которого получаем ответ}

function gen(k, s : word; var a : Square) : boolean;

var

i, j : integer;

CurS : word; { сколько единиц уже удалось поставить в квадрате KxK }

Begin

CurS:=0;

fillchar(a, sizeof(a), 0); {вначале заполняем квадрат нулями}

for i := 1 to k do

for j := 1 to k do

if CurS < s then {если число поставленных единиц меньше необходимого}

begin

a[i, j] := 1; {то ставим очередную единицу}

inc(CurS);

end

end;

if CurS < s then gen := false else gen := true;

end;




 if gen(k, s, a) then {генерируем образец}

for i := 1 to n do {заполняем образцом квадрат размером N*N}

begin {результат выводим сразу в файл}

for j := 1 to n do

write(a[(i-1) mod k+1,(j-1) mod k+1], ' ');

writeln;

end;
