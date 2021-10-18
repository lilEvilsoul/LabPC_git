function Get-TriangleArea{
    [CmdletBinding()] param([Parameter(Mandatory)] [int] $base, [Parameter(Mandatory)] [int] $altura)
    begin{
        Write-Host "Calcular area"
    }
    process{
        $area = ($base*$altura)/2
    }
    end{
        Write-Host "El area es: " $area
    }
}