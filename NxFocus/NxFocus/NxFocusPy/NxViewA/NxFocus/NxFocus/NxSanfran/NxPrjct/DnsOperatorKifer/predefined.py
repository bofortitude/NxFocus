#!/usr/bin/python


import dns.rdatatype

# bit 5	AA	Authoritative Answer	[RFC1035]
# bit 6	TC	Truncated Response	[RFC1035]
# bit 7	RD	Recursion Desired	[RFC1035]
# bit 8	RA	Recursion Available	[RFC1035]
# bit 9		Reserved
# bit 10	AD	Authentic Data	[RFC4035]
# bit 11	CD	Checking Disabled	[RFC4035]
flag_type_dict = {'QR': dns.flags.QR,
                  'AA': dns.flags.AA,
                  'TC': dns.flags.TC,
                  'RD': dns.flags.RD,
                  'RA': dns.flags.RA,
                  'AD': dns.flags.AD,
                  'CD': dns.flags.CD,
                  'DO': dns.flags.DO}


record_type_dict = {'NONE':dns.rdatatype.NONE,
                    'A':dns.rdatatype.A,
                    'NS':dns.rdatatype.NS,
                    'MD':dns.rdatatype.MD,
                    'MF':dns.rdatatype.MF,
                    'CNAME':dns.rdatatype.CNAME,
                    'SOA':dns.rdatatype.SOA,
                    'MB':dns.rdatatype.MB,
                    'MG':dns.rdatatype.MG,
                    'MR':dns.rdatatype.MR,
                    'NULL':dns.rdatatype.NULL,
                    'WKS':dns.rdatatype.WKS,
                    'PTR':dns.rdatatype.PTR,
                    'HINFO':dns.rdatatype.HINFO,
                    'MINFO':dns.rdatatype.MINFO,
                    'MX':dns.rdatatype.MX,
                    'TXT':dns.rdatatype.TXT,
                    'RP':dns.rdatatype.RP,
                    'AFSDB':dns.rdatatype.AFSDB,
                    'X25':dns.rdatatype.X25,
                    'ISDN':dns.rdatatype.ISDN,
                    'RT':dns.rdatatype.RT,
                    'NSAP':dns.rdatatype.NSAP,
                    'NSAP_PTR':dns.rdatatype.NSAP_PTR,
                    'SIG':dns.rdatatype.SIG,
                    'KEY':dns.rdatatype.KEY,
                    'PX':dns.rdatatype.PX,
                    'GPOS':dns.rdatatype.GPOS,
                    'AAAA':dns.rdatatype.AAAA,
                    'LOC':dns.rdatatype.LOC,
                    'NXT':dns.rdatatype.NXT,
                    'SRV':dns.rdatatype.SRV,
                    'NAPTR':dns.rdatatype.NAPTR,
                    'KX':dns.rdatatype.KX,
                    'CERT':dns.rdatatype.CERT,
                    'A6':dns.rdatatype.A6,
                    'DNAME':dns.rdatatype.DNAME,
                    'OPT':dns.rdatatype.OPT,
                    'APL':dns.rdatatype.APL,
                    'DS':dns.rdatatype.DS,
                    'SSHFP':dns.rdatatype.SSHFP,
                    'IPSECKEY':dns.rdatatype.IPSECKEY,
                    'RRSIG':dns.rdatatype.RRSIG,
                    'NSEC':dns.rdatatype.NSEC,
                    'DNSKEY':dns.rdatatype.DNSKEY,
                    'DHCID':dns.rdatatype.DHCID,
                    'NSEC3':dns.rdatatype.NSEC3,
                    'NSEC3PARAM':dns.rdatatype.NSEC3PARAM,
                    'TLSA':dns.rdatatype.TLSA,
                    'HIP':dns.rdatatype.HIP,
                    'SPF':dns.rdatatype.SPF,
                    'UNSPEC':dns.rdatatype.UNSPEC,
                    'TKEY':dns.rdatatype.TKEY,
                    'TSIG':dns.rdatatype.TSIG,
                    'IXFR':dns.rdatatype.IXFR,
                    'AXFR':dns.rdatatype.AXFR,
                    'MAILB':dns.rdatatype.MAILB,
                    'MAILA':dns.rdatatype.MAILA,
                    'ANY':dns.rdatatype.ANY,
                    'TA':dns.rdatatype.TA,
                    'DLV':dns.rdatatype.DLV}

record_class_dict = {'RESERVED0':dns.rdataclass.RESERVED0,
                     'IN':dns.rdataclass.IN,
                     'CH':dns.rdataclass.CH,
                     'HS':dns.rdataclass.HS,
                     'NONE':dns.rdataclass.NONE,
                     'ANY':dns.rdataclass.ANY}

rcode_reason_dict = {dns.rcode.NOERROR:'NOERROR',
                     dns.rcode.FORMERR:'FORMERR',
                     dns.rcode.SERVFAIL:'SERVFAIL',
                     dns.rcode.NXDOMAIN:'NXDOMAIN',
                     dns.rcode.NOTIMP:'NOTIMP',
                     dns.rcode.REFUSED:'REFUSED',
                     dns.rcode.YXDOMAIN:'YXDOMAIN',
                     dns.rcode.YXRRSET:'YXRRSET',
                     dns.rcode.NXRRSET:'NXRRSET',
                     dns.rcode.NOTAUTH:'NOTAUTH',
                     dns.rcode.NOTZONE:'NOTZONE',
                     dns.rcode.BADVERS:'BADVERS'}




