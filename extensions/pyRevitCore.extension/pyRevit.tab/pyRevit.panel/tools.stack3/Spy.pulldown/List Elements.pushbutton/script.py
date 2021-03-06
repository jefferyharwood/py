"""
Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'Lists specific elements from the model database.'

from Autodesk.Revit.DB import FilteredElementCollector, ElementMulticategoryFilter, BuiltInCategory, Element, ElementType, \
    GraphicsStyle, LinePatternElement, SketchPlane, View,\
                              ViewSheet, ModelArc, ModelLine, DetailArc, DetailLine, LogicalOrFilter, ModelPathUtils, \
                              TransmissionData, InstanceBinding, TypeBinding, FilteredWorksetCollector, \
                              WorksetKind
from Autodesk.Revit.DB.ExtensibleStorage import Schema
from Autodesk.Revit.UI import TaskDialog, PostableCommand, RevitCommandId
from System.Collections.Generic import List

from scriptutils.userinput import CommandSwitchWindow

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

selected_switch = CommandSwitchWindow(sorted(['Graphic Styles',
                                         'Grids',
                                         'Line Patterns',
                                         'Line Styles',
                                         'Selected Line Coordinates',
                                         'Model / Detail / Sketch Lines',
                                         'Project Parameters',
                                         'Data Schemas',
                                         'Data Schema Entities',
                                              'Sketch Planes',
                                              'Views',
                                              'View Templates',
                                              'Viewports',
                                              'Viewport Types',
                                              'Family Symbols',
                                              'Levels',
                                              'Scope Boxes',
                                              'Areas',
                                              'Rooms',
                                              'External References',
                                              'Revisions',
                                              'Revision Clouds',
                                              'Sheets',
                                              'System Categories',
                                              'System Postable Commands',
                                              'Worksets',
                                              ]), 'List elements of type:').pick_cmd_switch()


if selected_switch == 'Graphic Styles':
    cl = FilteredElementCollector(doc)
    gstyles = [i for i in cl.OfClass(GraphicsStyle).ToElements()]

    for gs in gstyles:
        if gs.GraphicsStyleCategory.Parent:
            parent = gs.GraphicsStyleCategory.Parent.Name
        else:
            parent = '---'
        if gs.GraphicsStyleCategory.GetHashCode() > 0:
            print('NAME: {0} CATEGORY:{2} PARENT: {3} ID: {1}'.format(gs.Name.ljust(50), gs.Id, gs.GraphicsStyleCategory.Name.ljust(50), parent.ljust(50)))

elif selected_switch == 'Grids':
    cl = FilteredElementCollector(doc)
    list = cl.OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()

    for el in list:
        print('GRID: {0} ID: {1}'.format(
            el.Name,
            el.Id,
        ))

elif selected_switch == 'Line Patterns':
    cl = FilteredElementCollector(doc).OfClass(LinePatternElement)
    for i in cl:
        print(i.Name)

elif selected_switch == 'Line Styles':
    c = doc.Settings.Categories.get_Item(BuiltInCategory.OST_Lines)
    subcats = c.SubCategories

    for lineStyle in subcats:
        print("STYLE NAME: {0} ID: {1}".format(lineStyle.Name.ljust(40), lineStyle.Id.ToString()))

elif selected_switch == 'Model / Detail / Sketch Lines':
    elfilter = ElementMulticategoryFilter(List[BuiltInCategory]([BuiltInCategory.OST_Lines, BuiltInCategory.OST_SketchLines]))
    cl = FilteredElementCollector(doc)
    cllines = cl.WherePasses(elfilter).WhereElementIsNotElementType().ToElements()

    for c in cllines:
        print('{0:<10} {1:<25}{2:<8} {3:<15} {4:<20}'.format(c.Id, c.GetType().Name, c.LineStyle.Id, c.LineStyle.Name,
                                                             c.Category.Name))

elif selected_switch == 'Project Parameters':
    pm = doc.ParameterBindings
    it = pm.ForwardIterator()
    it.Reset()
    while it.MoveNext():
        p = it.Key
        b = pm[p]
        if isinstance(b, InstanceBinding):
            bind = 'Instance'
        elif isinstance(b, TypeBinding):
            bind = 'Type'
        else:
            bind = 'Uknown'

        print('PARAM: {0:<10} UNIT: {1:<10} TYPE: {2:<10} GROUP: {3:<20} BINDING: {4}\nAPPLIED TO: {5}\n'.format(
            p.Name,
            str(p.UnitType),
            str(p.ParameterType),
            str(p.ParameterGroup),
            bind,
            [c.Name for c in b.Categories]
        ))

elif selected_switch == 'Data Schemas':
    for sc in Schema.ListSchemas():
        print('\n' + '-' * 100)
        print('SCHEMA NAME: {0}'
              '\tGUID:               {6}\n'
              '\tDOCUMENTATION:      {1}\n'
              '\tVENDOR ID:          {2}\n'
              '\tAPPLICATION GUID:   {3}\n'
              '\tREAD ACCESS LEVEL:  {4}\n'
              '\tWRITE ACCESS LEVEL: {5}'.format(sc.SchemaName,
                                                 sc.Documentation,
                                                 sc.VendorId,
                                                 sc.ApplicationGUID,
                                                 sc.ReadAccessLevel,
                                                 sc.WriteAccessLevel,
                                                 sc.GUID
                                                 ))
        if sc.ReadAccessGranted():
            for fl in sc.ListFields():
                print('\t\tFIELD NAME: {0}\n'
                      '\t\t\tDOCUMENTATION:      {1}\n'
                      '\t\t\tCONTAINER TYPE:     {2}\n'
                      '\t\t\tKEY TYPE:           {3}\n'
                      '\t\t\tUNIT TYPE:          {4}\n'
                      '\t\t\tVALUE TYPE:         {5}\n'.format(fl.FieldName,
                                                               fl.Documentation,
                                                               fl.ContainerType,
                                                               fl.KeyType,
                                                               fl.UnitType,
                                                               fl.ValueType
                                                               ))

elif selected_switch == 'Sketch Planes':
    cl = FilteredElementCollector(doc)
    skechplanelist = [i for i in cl.OfClass(SketchPlane).ToElements()]

    for gs in skechplanelist:
        print('NAME: {0} ID: {1}'.format(gs.Name.ljust(50), gs.Id))

elif selected_switch == 'Viewports':
    vps = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Viewports).WhereElementIsNotElementType().ToElements()

    for v in vps:
        print('ID: {1}TYPE: {0}VIEWNAME: {2}'.format(v.Name.ljust(30),
                                                     str(v.Id).ljust(10),
                                                     doc.GetElement(v.ViewId).ViewName
                                                     ))

elif selected_switch == 'Viewport Types':
    vps = []

    cl_views = FilteredElementCollector(doc)
    vptypes = cl_views.OfClass(ElementType).ToElements()

    for tp in vptypes:
        if tp.FamilyName == 'Viewport':
            print('ID: {1} TYPE: {0}'.format(Element.Name.GetValue(tp),
                                             str(tp.Id).ljust(10)
                                             ))

elif selected_switch == 'Family Symbols':
    cl = FilteredElementCollector(doc)
    symbollist = cl.OfClass(ElementType)

    for f in symbollist:
        print(Element.Name.GetValue(f), ElementType.FamilyName.GetValue(f))

elif selected_switch == 'Levels':
    levelslist = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()

    for i in levelslist:
        print('Level ID:\t{1}\tELEVATION:{2}\t\tName:\t{0}'.format(i.Name, i.Id.IntegerValue, i.Elevation))

elif selected_switch == 'Scope Boxes':
    scopeboxes = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_VolumeOfInterest).WhereElementIsNotElementType().ToElements()

    for el in scopeboxes:
        print('SCOPEBOX: {0}'.format(el.Name))

elif selected_switch == 'Areas':
    cl = FilteredElementCollector(doc)
    list = cl.OfCategory(BuiltInCategory.OST_Areas).WhereElementIsNotElementType().ToElements()

    for el in list:
        print('AREA NAME: {0} AREA NUMBER: {1} AREA ID: {2} LEVEL: {3} AREA: {4}'.format(
            el.LookupParameter('Name').AsString().ljust(30),
            el.LookupParameter('Number').AsString().ljust(10),
            el.Id,
            str(el.Level.Name).ljust(50),
            el.Area,
        ))

    print('\n\nTOTAL AREAS FOUND: {0}'.format(len(list)))

elif selected_switch == 'Rooms':
    cl = FilteredElementCollector(doc)
    list = cl.OfCategory(BuiltInCategory.OST_Rooms).WhereElementIsNotElementType().ToElements()

    for el in list:
        print('ROOM NAME: {0} ROOM NUMBER: {1} ROOM ID: {2}'.format(
            el.LookupParameter('Name').AsString().ljust(30),
            el.LookupParameter('Number').AsString().ljust(20),
            el.Id
        ))

    print('\n\nTOTAL ROOMS FOUND: {0}'.format(len(list)))

elif selected_switch == 'External References':
    location = doc.PathName
    try:
        modelPath = ModelPathUtils.ConvertUserVisiblePathToModelPath(location)
        transData = TransmissionData.ReadTransmissionData(modelPath)
        externalReferences = transData.GetAllExternalFileReferenceIds()
        for refId in externalReferences:
            extRef = transData.GetLastSavedReferenceData(refId)
            path = ModelPathUtils.ConvertModelPathToUserVisiblePath(extRef.GetPath())
            if '' == path:
                path = '--NOT ASSIGNED--'
            print("{0}{1}".format(str(str(extRef.ExternalFileReferenceType) + ':').ljust(20), path))
    except:
        print('Model is not saved yet. Can not aquire location.')

elif selected_switch == 'Revisions':
    cl = FilteredElementCollector(doc)
    revs = cl.OfCategory(BuiltInCategory.OST_Revisions).WhereElementIsNotElementType()

    for rev in revs:
        print('{0}\tREV#: {1}DATE: {2}TYPE:{3}DESC: {4}'.format(rev.SequenceNumber, str(rev.RevisionNumber).ljust(5),
                                                                str(rev.RevisionDate).ljust(10),
                                                                str(rev.NumberType.ToString()).ljust(15),
                                                                str(rev.Description).replace('\n', '').replace('\r', '')
                                                                ))

elif selected_switch == 'Sheets':
    cl_sheets = FilteredElementCollector(doc)
    sheetsnotsorted = cl_sheets.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
    sheets = sorted(sheetsnotsorted, key=lambda x: x.SheetNumber)

    for s in sheets:
        print('NUMBER: {0}   NAME:{1}'.format(s.LookupParameter('Sheet Number').AsString().rjust(10),
                                              s.LookupParameter('Sheet Name').AsString().ljust(50)
                                              ))

elif selected_switch == 'System Categories':
    for cat in doc.Settings.Categories:
        print(cat.Name)

elif selected_switch == 'System Postable Commands':
    for pc in PostableCommand.GetValues(PostableCommand):
        try:
            rcid = RevitCommandId.LookupPostableCommandId(pc)
            if rcid:
                print('{0} {1} {2}'.format(str(pc).ljust(50), str(rcid.Name).ljust(70), rcid.Id))
            else:
                print('{0}'.format(str(pc).ljust(50)))
        except:
            print('{0}'.format(str(pc).ljust(50)))

elif selected_switch == 'Views':
    selection = [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]

    views = []

    if len(selection) == 0:
        cl_views = FilteredElementCollector(doc)
        views = cl_views.OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
    else:
        for sel in selection:
            if isinstance(sel, View):
                views.append(sel)

    for v in views:
        phasep = v.LookupParameter('Phase')
        underlayp = v.LookupParameter('Underlay')
        print('TYPE: {1}ID: {2}TEMPLATE: {3}PHASE:{4} UNDERLAY:{5}  {0}'.format(
            v.ViewName,
            str(v.ViewType).ljust(20),
            str(v.Id).ljust(10),
            str(v.IsTemplate).ljust(10),
            phasep.AsValueString().ljust(25) if phasep else '---'.ljust(25),
            underlayp.AsValueString().ljust(25) if underlayp else '---'.ljust(25)
        ))

elif selected_switch == 'View Templates':
    cl_views = FilteredElementCollector(doc)
    views = cl_views.OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

    for v in views:
        if v.IsTemplate:
            print('ID: {1}		{0}'.format(v.ViewName, str(v.Id).ljust(10)))

elif selected_switch == 'Worksets':
    cl = FilteredWorksetCollector(doc)
    worksetlist = cl.OfKind(WorksetKind.UserWorkset)

    if doc.IsWorkshared:
        for ws in worksetlist:
            print('WORKSET: {0} ID: {1}'.format(ws.Name.ljust(50), ws.Id))
    else:
        TaskDialog.Show('pyRevit', 'Model is not workshared.')

elif selected_switch == 'Revision Clouds':
    cl = FilteredElementCollector(doc)
    revs = cl.OfCategory(BuiltInCategory.OST_RevisionClouds).WhereElementIsNotElementType()

    for rev in revs:
        parent = doc.GetElement(rev.OwnerViewId)
        if isinstance(parent, ViewSheet):
            print('REV#: {0}\t\tID: {3}\t\tON SHEET: {1} {2}'.format(doc.GetElement(rev.RevisionId).RevisionNumber,
                                                                     parent.SheetNumber,
                                                                     parent.Name,
                                                                     rev.Id
                                                                     ))
        else:
            print('REV#: {0}\t\tID: {2}\t\tON VIEW: {1}'.format(doc.GetElement(rev.RevisionId).RevisionNumber,
                                                                parent.ViewName,
                                                                rev.Id
                                                                ))

elif selected_switch == 'Selected Line Coordinates':
    def isline(line):
        if isinstance(line, ModelArc) or isinstance(line, ModelLine) or isinstance(line, DetailArc) or isinstance(line, DetailLine):
            return True
        return False


    for elId in uidoc.Selection.GetElementIds():
        el = doc.GetElement(elId)
        if isline(el):
            print('Line ID: {0}'.format(el.Id))
            print('Start:\t {0}'.format(el.GeometryCurve.GetEndPoint(0)))
            print('End:\t {0}\n'.format(el.GeometryCurve.GetEndPoint(1)))
        else:
            print('Elemend with ID: {0} is a not a line.\n'.format(el.Id))

elif selected_switch == 'Schema Entities':
    allElements = list(FilteredElementCollector(doc).WherePasses(
        LogicalOrFilter(ElementIsElementTypeFilter(False), ElementIsElementTypeFilter(True))))
    guids = {sc.GUID.ToString(): sc.SchemaName for sc in Schema.ListSchemas()}

    for el in allElements:
        schemaGUIDs = el.GetEntitySchemaGuids()
        for guid in schemaGUIDs:
            if guid.ToString() in guids.keys():
                print('ELEMENT ID: {0}\t\tSCHEMA NAME: {1}'.format(el.Id.IntegerValue, guids[guid.ToString()]))

    print('Iteration completed over {0} elements.'.format(len(allElements)))
