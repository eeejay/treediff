<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/sidebyside">
  <html>
    <head>
      <link rel="stylesheet" type="text/css" href="aria_list.css" />
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
    <xsl:apply-templates/> 
  </td>
</xsl:template>

<xsl:template match="right">
  <td>
    <xsl:apply-templates/> 
  </td>
</xsl:template>

<xsl:template match="accessible">
  <li>
    <a href="#" onclick="showDetails(this)" class="accessible">
      [<xsl:value-of select="@name"/>|<xsl:value-of select="@role"/>]
    </a>
    <table class="moreinfo">
      <tr>
        <td class="fieldname">Name:</td>
        <td class="fieldvalue"><xsl:value-of select="@name"/></td>
      </tr>
      <tr>
        <td class="fieldname">Role:</td>
        <td class="fieldvalue"><xsl:value-of select="@role"/></td>
      </tr>
      <tr>
        <td class="fieldname">Description:</td>
        <td class="fieldvalue"><xsl:value-of select="@description"/></td>
      </tr>
      <tr>
        <td class="fieldname">State:</td>
        <td class="fieldvalue"><xsl:value-of select="@state"/></td>
      </tr>
    </table>
        
    <xsl:if test="count(child::node())">
      <ul>
        <xsl:apply-templates/> 
      </ul>
    </xsl:if>
  </li>
</xsl:template>

</xsl:stylesheet>
