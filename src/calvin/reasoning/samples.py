"""
samples.py

* Copyright (c) 2006-2009, University of Colorado.
* All rights reserved.
*
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
*     * Redistributions of source code must retain the above copyright
*       notice, this list of conditions and the following disclaimer.
*     * Redistributions in binary form must reproduce the above copyright
*       notice, this list of conditions and the following disclaimer in the
*       documentation and/or other materials provided with the distribution.
*     * Neither the name of the University of Colorado nor the
*       names of its contributors may be used to endorse or promote products
*       derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE UNIVERSITY OF COLORADO ''AS IS'' AND ANY
* EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
* WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
* DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF COLORADO BE LIABLE FOR ANY
* DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
* (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
* ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
* (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
* SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import cscience.datastore

sample_list = []
landformData = {}
confidenceEntry = {}
#broken but only mildly
glacial = None
fluvial = None

samplePoll = []
landformPoll = []

initEnv = {}

landformQueue = []

_repomanager = None

__dataTypes = {'flat crested':'boolean', 'pitted':'boolean',
               'clast supported':'boolean', 'subject to prevailing winds':'boolean',
               'arid':'boolean', 'glacier length':'integer'}

def reset():
    global sample_list

    sample_list = []

def needData():
    return len(samplePoll) > 0 or len(landformPoll) > 0

def setRepoManager(repoman):
    global _repomanager
    _repomanager = repoman
    
def getFieldType(field):
    try:
        return datastore.sample_attributes[field].type_
    except KeyError:
        try:
            return __dataTypes[field]
        except KeyError:
            return None

def sampleMax(sampleA, sampleB, fld):
    if sampleA[fld] > sampleB[fld]:
        return sampleA
    else:
        return sampleB
    
def sampleMin(sampleA, sampleB, fld):
    if sampleA[fld] < sampleB[fld]:
        return sampleA
    else:
        return sampleB

def getLandformField(fld):
    try:
        return landformData[fld]
    except KeyError:
        if fld not in landformPoll and fld in __dataTypes:
            landformPoll.append(fld)
        raise KeyError()
    
def getSampleField(num, fld):
    return sample_list[num][fld]

def extractField(sample, fld):
    return sample[fld]

def getAllFlds(fld):
    return [sample[fld] for sample in sample_list]

def num_samples():
    return len(sample_list)

def isGlacial():
    """
    Checks if the landform is glacial first by whether it is a known type of glacial landform
    and then by polling the user if needed
    """
    global glacial
    if glacial is None:
        type = getLandformField('type')
        if type == 'moraine' or type.find('glaci') != -1 or type.find('erratic') != -1:
            res = True
        elif type.find('alluvial') != -1 or type.find('fluvial') != -1 or\
             type.find('river') != -1:
            res = False
        elif glacial is None:
            from calvin.gui import user_polling
            poll = user_polling.PromptDialog('is ' + type + ' a glacial landform?', 'boolean')
            res = poll.getResult()
            poll.Destroy()
        
        glacial = res
        
    return glacial
    
def isFluvial():
    """
    Checks if the landform is glacial first by whether it is a known type of glacial landform
    and then by polling the user if needed
    """
    global fluvial
    if fluvial is None:
        type = getLandformField('type')
        if type == 'moraine' or type.find('glaci') != -1 or type.find('erratic') != -1:
            res = False
        elif type.find('alluvial') != -1 or type.find('fluvial') != -1 or\
             type.find('river') != -1:
            res = True
        else:
            from calvin.gui import user_polling
            poll = user_polling.PromptDialog('is ' + type + ' a fluvial landform?', 'boolean')
            res = poll.getResult()
            poll.Destroy()
            
        fluvial = res
    
    return fluvial
getLandformField.userDisp = {'infix':False, 'text':'landform'}
getSampleField.userDisp = {'infix':False, 'text':'property of sample'}
extractField.userDisp = {'infix':False, 'text':'property of sample'}
num_samples.userDisp = {'infix':False, 'text':'number of samples'}
isGlacial.userDisp = {'infix':False, 'text':'glacial landform'}
isFluvial.userDisp = {'infix':False, 'text':'fluvial landform'}

