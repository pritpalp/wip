Install the commandlet for iLo
```powershell
Install-Module -Name HPEiLOCmdlets
```

Get a connection
```powershell
$Conn = Connect-HPEiLO -IP xxx -User xxx -Password xxx -DisableCertificateAuthentication
```

Use the connection to get storage controller info
```powershell
$HardDisks = Get-HPEiLOSmartArrayStorageController -Connection $Conn
```

Get the physical disk info
```powershell
$HardDisks.Controllers.PhysicalDrives
```

HP SSA Documentation: https://support.hpe.com/hpesc/public/docDisplay?docId=c03924344

SSA cmdline tools allows configuration of Smart Arrays

```ini
Action = Configure|Reconfigure 
Method = Custom Controller= All|Slot [N][:N] | WWN [N] | First | SerialNumber [N] | IOCabinet [N],IOBay [N],IOChassis [N],Slot [N],Cabinet [N],Cell [N] 
ClearConfigurationWithDataLoss = Yes|No|Forced 
LicenseKey = XXXXX-XXXXX-XXXXX-XXXXX-XXXXX 
DeleteLicenseKey = XXXXX-XXXXX-XXXXX-XXXXX-XXXXX 
ReadCache = 0|10|20|25|30|40|50|60|70|75|80|90|100 
WriteCache = 0|10|20|25|30|40|50|60|70|75|80|90|100 
RapidParityInitalization = Enable|Disable 
RebuildPriority = Low|Medium|Mediumhigh|High 
ExpandPriority = Low|Medium|High 
SurfaceScanDelay = N
SurfaceScanDelayExtended = N
SurfaceScanMode = Idle|High|Disabled 
MNPDelay = 0..60 
IRPEnable = Enable|Disable 
DPOEnable = Enable|Disable 
ElevatorSortEnable = Enable|Disable 
QueueDepth = 2|4|8|16|32|Automatic 
DriveWriteCache = Enable|Disable 
NoBatteryWriteCache = Enable|Disable 
PreferredPathMode = Auto|Manual 
BootVolumePrimary = Logical Drive Number|None 
BootVolumeSecondary = Logical Drive Number|None 
HBAMode = Enable|Disable 
PowerMode = MinPower|Balanced|MaxPerformance 
Latency = Disable|Low|High 

; Array Options 
; There can be multiple array specifications in the file 
Array = A|B|C|D|E|F|G|...Z|AA|AB|AC... | Next 
Drive = Port:ID... | Box:Bay... | Port:Box:Bay,... | N | * 
OnlineSpareMode = Dedicated | AutoReplace 
OnlineSpare = Port:ID,... | Box:Bay,... | Port:Box:Bay | None | N 
SplitMirror = SplitWithBackup|Rollback|Remirror|ActivateBackup 

; Caching Array Options 
; There can be only one Caching Array specification in the file 
CachingArray = A|B|C|D|E|F|...Z|AA|AB|AC... 
Drive = Port:ID,... | Box:Bay,... | Port:Box:Bay,... 

; Logical Drive Options 
; There can be multiple logical drive specifications in the file 
; The maximum strip size depends on the number of drives in an array and the size of the controller cache 
LogicalDrive = 1|2|3... max Volumes | Next 
Repeat = 0... max Volumes 
RAID = 0|1|10|5|6|ADG|50|60 
Size = N|Max|MAXMBR 
SizeBocks = N 
NumberOfParityGroups = N 
Sectors = 32|63 
StripSize = 8|16|32|64|128|256|512|1024 
ArrayAccelerator = Enable|Disable 
SSDOverProvisioningOptimization = Enable|Disable OPTIONAL: 
Renumber = N OPTIONAL: 
SetBootVolumePrimary = Enable OPTIONAL: 
SetBootVolumeSecondary = Enable 

; Caching Logical Drive Options 
CachingLogicalDrive = 1|2|3... max Volumes/2 
RAID = 0|1 ;FW and Controller dependent 
Size = N 
CachedLogicalDrive = Logical Drive Number
```

