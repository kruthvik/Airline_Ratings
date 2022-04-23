$add = New-Object System.Management.Automation.Host.ChoiceDescription '&add', 'Command: add'
$get = New-Object System.Management.Automation.Host.ChoiceDescription '&get', 'Command: get'
$help = New-Object System.Management.Automation.Host.ChoiceDescription '&help', 'Command: help'
$list = New-Object System.Management.Automation.Host.ChoiceDescription '&list', 'Command: list'
$mode = New-Object System.Management.Automation.Host.ChoiceDescription '&mode', 'Command: mode'
$ratings = New-Object System.Management.Automation.Host.ChoiceDescription '&ratings', 'Command: ratings'
$update = New-Object System.Management.Automation.Host.ChoiceDescription '&update', 'Command: update'

$options = [System.Management.Automation.Host.ChoiceDescription[]]($add, $get, $help, $list, $mode, $ratings, $update)

$title = 'Choose Command'
$message = 'What command do you want to run?'
$result = $host.ui.PromptForChoice($title, $message, $options, 0)

[System.Collections.ArrayList]$list = @("add", "get", "help", "list", "mode", "ratings", "update")
$command = $list[$result]

write-output "The command you chose was: $command"

if ($command -eq "update") {
    py main.py
    exit
}

if("get help list mode".contains($command)) {
    py main.py -c $command
} else {
    $data = @()
    while ($true) {
        $value = Read-Host "Enter airplane input (\q to stop) (enter to finalize)"
        if ('' -eq $value) {
            break
        }

        if (('\q' -eq $value) -or ('\Q' -eq $value)) {
            exit
        }

        $data += $value
    }
    $data = $data -join " "
    py main.py -c $command -a $data
}
