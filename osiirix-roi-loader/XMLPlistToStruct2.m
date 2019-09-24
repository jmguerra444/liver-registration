function [S, KT] = XMLPlistToStruct2(xml)
% XMLPlistToStruct  Parse Mac OSX XML property list into matlab structure
%
%   S = XMLPlistToStruct(xmlText)
%
%       return structure S from OS X style XML property list in string xmlText
%
%           The mapping is straightforward:
%           dict -> structure
%           array -> cell array
%           property list keys become field names
%               (note: keys may only contain alphanumeric or space chars)
%           integer, real -> double
%           string, data, date -> string
%
%       Note: data and date are treated as strings, with a suffix (_DATA or
%               _DATE) added to the field name indicating the original type, 
%               similarly _INTEGER is added for integers. This ensures
%               that the original type is preserved if we convert the 
%               structure back to XML.
%
%   See the example plist and usage at the end of this file
%
%   Details of XML property list format are found at:
%   http://developer.apple.com/documentation/Cocoa/Conceptual/PropertyLists/Concepts/XMLPListsConcept.html
%   http://www.apple.com/DTDs/PropertyList-1.0.dtd
%
%   JRI 3/14/05 (John R. Iversen <iversen@nsi.edu>)

dictLevel = 0;
inArray = 0;
arrayIndex = 0;
key = {};

ibra = findstr(xml,'<');
iket = findstr(xml,'>');

if (length(ibra) ~= length(iket))
    error('unmatched brackets')
end

itag = 1;
ikey =1;

expr='';
KT{1,2} = '';
usedname={{}};
arraylv=0;
while (itag <= length(ibra))
    
    value = [];
    valueStr = '';
    keySuffix = '';
    tag = xml( (ibra(itag)+1):(iket(itag)-1) );
    
    %split tag on first space into tag proper and additional information
    iSpace = strfind(tag, ' ');
    if ~isempty(iSpace)
        tagInfo = tag( (iSpace(1)+1):end );
        tag = tag(1:(iSpace(1)-1));
    end
    
    %if we're in an array, increase the index by one
%     if (dictLevel > 0) & inArray(dictLevel),
%        arrayIndex(dictLevel) = arrayIndex(dictLevel) + 1;
%     end

    switch tag
        
        case '!DOCTYPE'  %make sure it's a plist
            if isempty(findstr(tagInfo, 'plist'))
                error('This is not an Apple plist')
            end
                
        case {'?xml', 'plist', '/plist'}
            %skip other header tags--assume they, as well as outer <plist></plist>, are correct
            
        case 'dict'
            
            expr=[expr 'struct('];
            
            dictLevel = dictLevel + 1;
%             inArray(dictLevel) = 0;
            arraylv(dictLevel)=0;
            usedname{dictLevel}={};
        case '/dict'
            expr=[expr(1:end-1) '),']; % delete ","

            
%             key(dictLevel) = [];
%             if (inArray(dictLevel) ~= 0), error('Array not closed by end of dict'); end
             dictLevel = dictLevel - 1;
%             usedname(dictLevel) = {};
        case 'key'
            keyname = xml( (iket(itag)+1):(ibra(itag+1)-1) );
            fieldname = genvarname(keyname,usedname{dictLevel});% generate valid variable name.
            usedname{dictLevel}{end+1} = fieldname;
            KT{ikey,1} = keyname;
            KT{ikey,2} = fieldname;

%            KT{ikey,2} = key{dictLevel};

            ikey = ikey + 1;
            itag = itag + 1; %skip to close
            ctag = xml( (ibra(itag)+1):(iket(itag)-1) );
            if ~strcmp(ctag, ['/' tag]), error(['<' tag '> not properly closed']); end
            expr = [expr '''' fieldname ''',' ];
            
        case 'array'
%             
            if arraylv(dictLevel) ==0
                expr = [expr '{{'];
            else
                expr = [expr '{'];
            end
%             expr = [expr '{'];            
            arraylv(dictLevel) = arraylv(dictLevel) + 1;
%             inArray(dictLevel) = inArray(dictLevel) +1;
%             arrayIndex(dictLevel) = 0;
%             arraystr = [arraystr '{'];
            
        case '/array'
            arraylv(dictLevel) = arraylv(dictLevel) - 1;
            if arraylv(dictLevel) ==0
                expr = [expr '}},'];
            else
                expr = [expr '},'];
            end
            

%             inArray(dictLevel) = inArray(dictLevel) +1;
%             arrayIndex(dictLevel) = 0;
%             arraystr = [arraystr '}'];

        case 'array/' %empty array
            expr = [expr '{{[]}},'];

%             value = { [] };
                
        case 'true/'
            
           expr = [expr 'true,'];

%             value = true; %logical

        case 'false/'
            expr = [expr 'false,'];

%             value = false; %logical

        case {'string', 'date', 'data'}
            valueStr = xml( (iket(itag)+1):(ibra(itag+1)-1) );           
            str = sprintf('c%s(''%s''),',upper(tag), valueStr);
            expr = [expr str];
%           valueStr = feval(sprintf('c%s',upper(tag)), valueStr);
            
            itag = itag + 1; %skip to close
            closetag = xml( (ibra(itag)+1):(iket(itag)-1) );
            if ~strcmp(closetag, ['/' tag]), error(['<' tag '> not properly closed']); end


        case {'integer', 'real'}
            valueStr = xml( (iket(itag)+1):(ibra(itag+1)-1) );
            value = str2num(valueStr);
            itag = itag + 1; %skip to close
            closetag = xml( (ibra(itag)+1):(iket(itag)-1) );
            if ~strcmp(closetag, ['/' tag]), error(['<' tag '> not properly closed']); end
            %add suffix to indicate original type
            if strcmp(tag, 'integer')
                str =sprintf('int32(%d),',value);
            else
                str =sprintf('%.100g,',value);
            end
            expr = [expr str];
        otherwise
            error(['Unexpected tag: ' tag])
                      
    end

    itag = itag+1;
            
end

expr=regexprep(expr,char(10),'');
expr=regexprep(expr,char(13),'');
expr=regexprep(expr,'\t','');

S = eval(expr);
if (dictLevel > 0) || any(inArray)
    error('unfinished dict or array, but now at end of file')
end