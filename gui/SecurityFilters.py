"""
Copyright 2020 Sergio Espinoza Lopez sergio.espinoza.lopez@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


  Convenience data class for holding several security screening

"""

from dataclasses import dataclass
from typing import ClassVar

from typing import Dict, TypeVar, ClassVar

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ElementTree, Element


Element_t = TypeVar( "Element")

class SecurityFilters:

    #short descpriptions for each filter parameter
    shortDesc : ClassVar[ Dict[ str, str ] ] = {
        "minMarketCap" : "Scan % under Px",
        "constituentsSlice" : "No. mothly expiries",
        "minOptionVolume" : "Max loss",
        "minIvRank" : "Min Profit",
        "minDaysToEarnigns": "Mini days to earnings"

    }



    # storing tool tips on parameter entries
    toolTips : ClassVar[ Dict[ str, str ] ] = {
        "minMarketCap" : "Minimum market capital in USDM$",

        "constituentsSlice" : "Limit scaning to this number \
                                of securities after ordering \
                                top to bottom by market cap",

        "minOptionVolume" : "Minimum average daily option \
                               volume",

        "minIvRank" : "52 weeks implied volatility rank",

        "minDaysToEarnigns" :  "Minimum days to next earnings \
                                   report"
    }

    #this method should be created via @dataclass annotation
    #as well, but adding for documentation purposes
    def __init__( self, minMarketCap : float = 2000 ,
                        constituentsSlice : float = 11,
                        minOptionVolume : float = 10,
                        minIvRank : float = 10,
                        minDaysToEarnigns : float = 25 ):
        """
            parameters:

            minMarketCap : minimum market capital in USD Millions Dollars

            constituentsSlice: After minimum market cap ordering  and filtering
                                scan up to to this number of securities

            minOptionVolume: minimum average daily option volume

            minIvRank: 52 weeks Implied Volatility Rank (%)

            minDaysToEarnigns: minimum days to next earnings report

        """
        self.minMarketCap = minMarketCap
        self.constituentsSlice = constituentsSlice
        self.minOptionVolume = minOptionVolume
        self.minIvRank = minIvRank
        self.minDaysToEarnigns = minDaysToEarnigns



    def loadFromXmlElem( self, elementSubTree : Element_t  ):
        """
            Initialize using xml subtree (Element) of 'underlyings' tag

            arguments:
                elementSubTree: xml 'element' including the 'underlyings'
                                tag and its sub-tree
        """

        underlyingsEl = element.find( 'underlyings' )

        if underlyingsEl is not None:
            for parameter in underlyingsEl.findall ( 'parameter' ):
                nameEl = parameter.find( 'name' )
                valueEl = parameter.find( 'value' )
                try:
                    #attribute name should be the same as
                    #the xml tag
                    setattribute( nameEl.text, valueEl.text )

                except:
                    logging.error( 'parameter not found, unable to load values from \
                                 xml' )

    def saveToXmlElem( self, elementSubTree : Element_t ):
        """
        Save to xml tree Element
            arguments
                element: Empty element sub-tree at which to save parameters.
                         'underlyings' and sub-tree will be created
        """
        underlyingsEl = elementSubTree.Element( 'underlyings' )

        for attributeName  in dir(self):
            attributeValue = getattribute( self,  attributeName )
            #create new parameter
            parameterElement = underlyingsEl.Element( 'parameter' )

            nameElement = parameterElement.Element( 'name' )
            nameElement.text = attributeName
            #assign value
            valueEl = parameterElement.subElement( 'value' )
            valueEl.text = attributeValue