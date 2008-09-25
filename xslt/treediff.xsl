<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
                xmlns:revtree="http://monotonous.org">

<xsl:template match="/sidebyside">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="treediff.css" />
      <script type="text/javascript" src="aria_list.js" />
      <title>An Experiment</title>
    </head>
    <body>
      <table border="1">
        <tr>
          <xsl:apply-templates/> 
        </tr>
      </table>
    </body>
  </html>
</xsl:template>

<xsl:template match="left">
  <td>
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="right">
  <td>
    <ul>
      <xsl:apply-templates/> 
    </ul>
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li>
    <xsl:variable name="baseclass">accessiblenode</xsl:variable>
	<xsl:choose>

	  <xsl:when test="contains(@revtree:changes, 'moved-self')">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revMoved')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(@revtree:changes, 'deleted-self')">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revDeleted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(@revtree:changes, 'inserted-self')">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revInserted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:otherwise>
		<xsl:attribute name="class">
		  <xsl:value-of select="$baseclass"/>
		</xsl:attribute> 
	  </xsl:otherwise>

  </xsl:choose>	
    <b>[</b><xsl:apply-templates select="@name"/> •
    <xsl:apply-templates select="@role"/> • 
    <xsl:apply-templates select="@description"/> •
    <xsl:apply-templates select="@state"/><b>]</b> 
    <xsl:if test="count(child::*)">
      <ul>
        <xsl:apply-templates/> 
      </ul>
    </xsl:if>
  </li>
</xsl:template>

<xsl:template match="@*">
  <span>
	<xsl:variable name="baseclass" 
                  select="concat('accessible', name())"/>
	<xsl:choose>
	  <xsl:when test="contains(../@revtree:updatedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revUpdated')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(../@revtree:deletedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revDeleted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:when test="contains(../@revtree:insertedAttribs, name())">
		<xsl:attribute name="class">
		  <xsl:value-of select="concat($baseclass,' revInserted')"/>
		</xsl:attribute> 
	  </xsl:when>

	  <xsl:otherwise>
		<xsl:attribute name="class">
		  <xsl:value-of select="$baseclass"/>
		</xsl:attribute> 
	  </xsl:otherwise>

  </xsl:choose>	
	<xsl:value-of select="."/>
  </span>
</xsl:template>

</xsl:stylesheet>
