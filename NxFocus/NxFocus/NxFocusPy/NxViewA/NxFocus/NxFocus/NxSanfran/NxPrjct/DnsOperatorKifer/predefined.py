#!/usr/bin/python


# import dns.rdatatype
from NxSanfran.NxLib.dns import rdatatype
from NxSanfran.NxLib.dns import flags

# bit 5	AA	Authoritative Answer	[RFC1035]
# bit 6	TC	Truncated Response	[RFC1035]
# bit 7	RD	Recursion Desired	[RFC1035]
# bit 8	RA	Recursion Available	[RFC1035]
# bit 9		Reserved
# bit 10	AD	Authentic Data	[RFC4035]
# bit 11	CD	Checking Disabled	[RFC4035]
flag_type_dict = {'QR': flags.QR,
                  'AA': flags.AA,
                  'TC': flags.TC,
                  'RD': flags.RD,
                  'RA': flags.RA,
                  'AD': flags.AD,
                  'CD': flags.CD,
                  'DO': flags.DO}


record_type_dict = {'NONE':rdatatype.NONE,
                    'A':rdatatype.A,
                    'NS':rdatatype.NS,
                    'MD':rdatatype.MD,
                    'MF':rdatatype.MF,
                    'CNAME':rdatatype.CNAME,
                    'SOA':rdatatype.SOA,
                    'MB':rdatatype.MB,
                    'MG':rdatatype.MG,
                    'MR':rdatatype.MR,
                    'NULL':rdatatype.NULL,
                    'WKS':rdatatype.WKS,
                    'PTR':rdatatype.PTR,
                    'HINFO':rdatatype.HINFO,
                    'MINFO':rdatatype.MINFO,
                    'MX':rdatatype.MX,
                    'TXT':rdatatype.TXT,
                    'RP':rdatatype.RP,
                    'AFSDB':rdatatype.AFSDB,
                    'X25':rdatatype.X25,
                    'ISDN':rdatatype.ISDN,
                    'RT':rdatatype.RT,
                    'NSAP':rdatatype.NSAP,
                    'NSAP_PTR':rdatatype.NSAP_PTR,
                    'SIG':rdatatype.SIG,
                    'KEY':rdatatype.KEY,
                    'PX':rdatatype.PX,
                    'GPOS':rdatatype.GPOS,
                    'AAAA':rdatatype.AAAA,
                    'LOC':rdatatype.LOC,
                    'NXT':rdatatype.NXT,
                    'SRV':rdatatype.SRV,
                    'NAPTR':rdatatype.NAPTR,
                    'KX':rdatatype.KX,
                    'CERT':rdatatype.CERT,
                    'A6':rdatatype.A6,
                    'DNAME':rdatatype.DNAME,
                    'OPT':rdatatype.OPT,
                    'APL':rdatatype.APL,
                    'DS':rdatatype.DS,
                    'SSHFP':rdatatype.SSHFP,
                    'IPSECKEY':rdatatype.IPSECKEY,
                    'RRSIG':rdatatype.RRSIG,
                    'NSEC':rdatatype.NSEC,
                    'DNSKEY':rdatatype.DNSKEY,
                    'DHCID':rdatatype.DHCID,
                    'NSEC3':rdatatype.NSEC3,
                    'NSEC3PARAM':rdatatype.NSEC3PARAM,
                    'TLSA':rdatatype.TLSA,
                    'HIP':rdatatype.HIP,
                    'SPF':rdatatype.SPF,
                    'UNSPEC':rdatatype.UNSPEC,
                    'TKEY':rdatatype.TKEY,
                    'TSIG':rdatatype.TSIG,
                    'IXFR':rdatatype.IXFR,
                    'AXFR':rdatatype.AXFR,
                    'MAILB':rdatatype.MAILB,
                    'MAILA':rdatatype.MAILA,
                    'ANY':rdatatype.ANY,
                    'TA':rdatatype.TA,
                    'DLV':rdatatype.DLV}

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




