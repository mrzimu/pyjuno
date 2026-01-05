# pyjuno

Pyjuno is a Python package that helps JUNO users analyzing data more easily. The core functionality of pyjuno is its JUNO-specific format data reading.

> ![WARNING]
> This package is still under developing.

## Installation

```bash
pip install pyjuno
```

> [!TIP]
> If you are working on IHEP computing nodes (lxlogin server), it is recommended to move `~/.local` and `~/.cache` to somewhere else, in case of the installation reaches your disk quota in `/afs` file system.

## JUNO format data reading

Basing on [Uproot](https://uproot.readthedocs.io/), [uproot-custom](https://mrzimu.github.io/uproot-custom/index.html) and [awkward-array](https://awkward-array.org/doc/main/user-guide/index.html), pyjuno can read most of JUNO-specific data format without ROOT or junosw environment.

> [!NOTE]
> At present, `GenEvent` is not supported to be read in Python, since it contains recursive data that awkward-array cannot handle with.

### Standalone subevent reading

```python
>>> import uproot
>>> import pyjuno # automatically register JUNO format to uproot
>>> f = uproot.open("rec.root")
>>> calib_pmt = f["Event/CdLpmtCalib/CdLpmtCalibEvt/m_calibPMTCol"].array()
>>> calib_pmt.show()
[[{m_nPE: 0.842, m_pmtId: 269619712, m_firstHitTime: 386, ...}, ..., {...}],
 [{m_nPE: 0.427, m_pmtId: 269500928, m_firstHitTime: 433, ...}, ..., {...}],
 [{m_nPE: 0.751, m_pmtId: 269500928, m_firstHitTime: 385, ...}, ..., {...}],
 [{m_nPE: 1.04, m_pmtId: 269558272, m_firstHitTime: 387, ...}, ..., {...}],
 [{m_nPE: 2.41, m_pmtId: 269500928, m_firstHitTime: 979, ...}, ..., {...}],
 [{m_nPE: 3.9, m_pmtId: 269586944, m_firstHitTime: 899, ...}, ..., {...}],
 [{m_nPE: 1.33, m_pmtId: 269615616, m_firstHitTime: 673, ...}, ..., {...}],
 [{m_nPE: 0.539, m_pmtId: 269496832, m_firstHitTime: 401, ...}, ..., {...}],
 [{m_nPE: 0.478, m_pmtId: 269554176, m_firstHitTime: 377, ...}, ..., {...}],
 [{m_nPE: 0.554, m_pmtId: 269496832, m_firstHitTime: 389, ...}, ..., {...}]]
```

### Assembling all subevents

In JUNO, subevents are not always present in one event. To assemble different subevent tree, a method `pyjuno.assemble_event` is provided:

```python
>>> import uproot
>>> import pyjuno # automatically register JUNO format to uproot
>>> f = uproot.open("rec.root")
>>> events = pyjuno.assemble_event(f)
>>> events.show()
[{SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...},
 {SimEvt: [{m_tracks: [{...}], ...}], CdLpmtElecTruthEvt: [[...]], ...}]
```

Reading all data from file at once could consume much memory. You can either read less events by specifying `entry_start` and `entry_stop` arguments, or only read necesarry subevents by passing `filter_path` argument:

```python
# Read a small batch of events
batch_events = pyjuno.assemble_event(f, entry_start=0, entry_stop=10)

# Read CdLpmtTruth and CdSpmtTruth
spec_events = pyjuno.assemble_event(f, filter_path=["/Event/CdLpmtTruth", "/Event/CdSpmtTruth"])
# or
spec_events = pyjuno.assemble_event(f, filter_path="*pmtTruth")
```
