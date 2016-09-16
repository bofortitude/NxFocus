#!/usr/bin/python


import os


PreDefaultScriptPath = os.path.split(os.path.realpath(__file__))[0]
originalWorkingPath = os.getcwd()
os.chdir(PreDefaultScriptPath)
os.chdir('..')
#NxPublicConfigPredefinedPath = os.getcwd()
NxEtcPublicPath = os.getcwd()
os.chdir('..')
NxSanfranEtcPath = os.getcwd()
os.chdir('..')
NxFocusSanfranPath = os.getcwd()
os.chdir('..')
NxFocusPath = os.getcwd()
os.chdir(originalWorkingPath)



NxFocusInputPath = NxFocusPath+'/NxInput'
NxInputPrjctsPath = NxFocusInputPath+'/NxPrjcts'
NxFocusOutputPath = NxFocusPath+'/NxOutput'
NxOutputPrjctsPath = NxFocusOutputPath+'/NxPrjcts'

NxSanfranBinPath = NxFocusSanfranPath+'/NxBin'
#NxSanfranEtcPath = NxFocusSanfranPath+'/NxEtc'
NxSanfranLibPath = NxFocusSanfranPath+'/NxLib'
NxSanfranPrjctPath = NxFocusSanfranPath+'/NxPrjct'
NxSanfranRunPath = NxFocusSanfranPath+'/NxRun'
NxSanfranTmpPath = NxFocusSanfranPath+'/NxTmp'
NxSanfranToolsPath = NxFocusSanfranPath+'/NxTools'
NxSanfranUsrPath = NxFocusSanfranPath+'/NxUsr'
NxSanfranVarPath = NxFocusSanfranPath+'/NxVar'

NxBinPrjctsPath = NxSanfranBinPath+'/NxPrjcts'

NxEtcPrjctsPath = NxSanfranEtcPath+'/NxPrjcts'
#NxEtcPublicPath = NxSanfranEtcPath+'/NxPublic'
#NxEtcPublicPath = NxSanfranEtcPath+'/NxPublic'
NxPublicConfPath = NxEtcPublicPath+'/NxConf'
NxPublicPredefaultPath = NxEtcPublicPath+'/NxPredefault'
NxPublicXmlPath = NxEtcPublicPath+'/NxXml'

NxTmpPrjctsPath = NxSanfranTmpPath+'/NxPrjcts'

NxUsrLibPath = NxSanfranUsrPath+'/NxLib'
NxUsrLocalPath = NxSanfranUsrPath+'/NxLocal'
NxUsrSharePath = NxSanfranUsrPath+'/NxShare'
NxShareManPath = NxUsrSharePath+'/NxMan'
NxUsrSrcPath = NxSanfranUsrPath+'/NxSrc'

NxVarInputPath = NxSanfranVarPath+'/NxInput'
NxVarOutputPath = NxSanfranVarPath+'/NxOutput'
NxVarLogPath = NxSanfranVarPath+'/NxLog'
NxVarResourcesPath = NxSanfranVarPath+'/NxResources'
NxLogPrjctsPath = NxVarLogPath+'/NxPrjcts'



