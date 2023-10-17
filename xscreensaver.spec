%define disable_inappropriate 0

Summary:	A set of X Window System screensavers
Name:		xscreensaver
Version:	6.08
Release:	1
License:	BSD
Group:		Graphical desktop/Other
URL:		http://www.jwz.org/xscreensaver/
Source0:	http://www.jwz.org/xscreensaver/%{name}-%{version}.tar.gz
Source1:	xscreensaver-capplet.png
Source2:	dmctl
Source3:	update-xscreensaver-hacks
Patch0:		xscreensaver-5.05-mdv-alt-drop_setgid.patch
# Don't check login manager in PATH because we use custom wrapper
#Patch1:		xscreensaver-5.15-lmcheck.patch
# Only OpenMandriva should be enabled
Patch9:		xscreensaver-5.45-defaultconfig.patch
# (fc) 4.05-3mdk disable openGL hacks by default
#Patch11:	xscreensaver-5.09-noGL.patch

# fedora patches
# bug 129335
# sanitize the names of modes in barcode
Patch1001:	xscreensaver-5.44-sanitize-hacks.patch
## Patches already sent to the upsteam
## Patches which must be discussed with upstream
#
# Change webcollage not to access to net
# Also see bug 472061
Patch1021:	xscreensaver-6.06-webcollage-default-nonet.patch
#

Requires:	xscreensaver-common = %{version}-%{release}
#Requires:	fortune-mod
Requires:	distro-release-theme
Requires:	xdg-utils
Requires:	pam >= 1.1.8-19
BuildRequires:	intltool
BuildRequires:	bc
#BuildRequires:	fortune-mod
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:	pkgconfig(krb5)
BuildRequires:  pkgconfig(gtk+-3.0) >= 2.22.0
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xinerama)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xxf86misc)
BuildRequires:	pkgconfig(xxf86vm)
BuildRequires:	pkgconfig(xft)
BuildRequires:	gle-devel
BuildRequires:	imagemagick
BuildRequires:	xdg-utils

%description
The xscreensaver package contains a variety of screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure.

Install the xscreensaver package if you need screensavers for use with
the X Window System.

%package base
Summary:	A set of screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}
Conflicts:	xscreensaver < 5.00-2
Requires:	words

%description base
Various screensavers used by Xscreensaver.

%package common
Summary:	Utilities used by xscreensaver screensavers
Group:		Graphical desktop/Other
Conflicts:	xscreensaver < 5.26-2
Provides:	xscreensaver-utils

%description common
Utilities used by xscreensaver screensavers.

%package gl
Summary:	A set of GL screensavers
Group:		Graphical desktop/Other
Requires:	xscreensaver-common = %{version}-%{release}
Requires(post):	xscreensaver-common = %{version}-%{release}
Requires(postun):	xscreensaver-common = %{version}-%{release}
%rename		%{name}-extrusion
%rename		%{name}-matrix

%description gl
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.

%prep
%setup -q
#patch1 -p1 -b .login-manager
# WARNING this patch must ALWAYS be applied, if it fails, REGENERATE it !!!
%patch9 -p1 -b .defaultconfig
#%patch11 -p1 -b .noGL
%if %{disable_inappropriate}
%patch1001 -p1 -b .inappropriate
%endif

%patch1021 -p1

# Needed by patches 1 and 11
#autoreconf -fiv

# Fix the %%configure-breaking
# ac_unrecognized_opts check
sed -i -e '/exit 2$/d' configure.ac configure

%build
%configure \
	--enable-locking \
	--enable-root-passwd \
	--with-browser=xdg-open \
	--with-dpms-ext \
	--with-xinerama-ext \
	--with-xf86vmode-ext \
	--with-xf86gamma-ext \
	--with-randr-ext \
	--with-login-manager=dmctl \
	--without-shadow \
	--with-pixbuf \
	--with-jpeg \
	--with-xshm-ext \
	--with-xdbe-ext \
	--without-setuid-hacks \
	--with-gtk \
	--without-motif \
	--with-pam \
	--enable-pam-check-account-type \
	--with-gl \
	--with-image-directory=%{_datadir}/mdk/screensaver \
	--without-kerberos \
	--with-text-file=%{_sysconfdir}/release \
	--with-gle

%make 

%install
rm -rf %{buildroot} gl-extras.files base.files %{name}.lang
mkdir -p %{buildroot}%{_sysconfdir}/X11/app-defaults/
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man6
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_libexecdir}/xscreensaver
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart

make install_prefix=%{buildroot} bindir=%{_bindir} \
 KDEDIR=%{_prefix} GNOME_BINDIR=%{_bindir}  GNOME_DATADIR=%{_datadir} \
 mandir=%{_mandir} AD_DIR=%{_datadir}/X11/app-defaults/ \
 gnulocaledir=%{_datadir}/locale install
%makeinstall -C po

install -p -m755 %{SOURCE3} -D %{buildroot}%{_sbindir}/update-xscreensaver-hacks

# Custom wrapper for gdmflexiserver and kdmctl
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/dmctl

cat<<EOF >README.GL
The xscreensaver-gl package contains even more screensavers for your
mind-numbing, ambition-eroding, time-wasting, hypnotized viewing
pleasure. These screensavers require OpenGL or Mesa support.

Install the xscreensaver-gl package if you need more screensavers for
use with the X Window System and you have OpenGL or Mesa installed.
EOF

cat >%{buildroot}%{_sysconfdir}/xdg/autostart/xscreensaver.desktop <<EOF
[Desktop Entry]
Name=XScreenSaver
Exec=xscreensaver -nosplash
Icon=xscreensaver
Terminal=False
Type=Application
X-KDE-StartupNotify=False
OnlyShowIn=X-NODEFAULT;
EOF

#icons
mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
cp %{SOURCE1}  %{buildroot}%{_datadir}/pixmaps
convert -scale 16x16 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
convert -scale 32x32 %{SOURCE1} %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
ln -s %{_datadir}/pixmaps/xscreensaver-capplet.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

# This function prints a list of things that get installed.
# It does this by parsing the output of a dummy run of "make install".
#
list_files() {
  make -s install_prefix=%{buildroot} mandir=%{_mandir}/ \
  bindir=%{_bindir} INSTALL=true "$@"	\
   | sed -n -e 's@.* \(/[^ ]*\)$@\1@p'				\
   | sed    -e "s@^%{buildroot}@@"				\
	    -e "s@/[a-z][a-z]*/\.\./@/@"			\
   | sed    -e 's@\(.*/man/.*\)@\1\*@'				\
   | sed    -e 's@\(.*/app-defaults/\)@%config \1@'		\
	    -e 's@\(.*/pam\.d/\)@%config(missingok) \1@'	\
   | sort
}

# Generate three lists of files for the three packages.
#
dd=%{_builddir}/%{name}-%{version}
pushd hacks/glx ; list_files install > $dd/gl-extras.files ; popd
pushd hacks     ; list_files install > $dd/base.files; popd

%post gl
sed -i -e 's/\A-\s+GL:/ GL:/' %{_datadir}/X11/app-defaults/XScreenSaver

%postun gl
sed -i -e '/\A\s*GL:/ and print "- $_" or print "$_"' %{_datadir}/X11/app-defaults/XScreenSaver

%files
%doc README
%config(noreplace) %{_sysconfdir}/pam.d/xscreensaver
#%%doc %{_mandir}/man1/xscreensaver-systemd.1*
%doc %{_mandir}/man1/xscreensaver-command.1*
%doc %{_mandir}/man1/xscreensaver-demo.1*
%doc %{_mandir}/man1/xscreensaver.1*
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%attr(755,root,shadow) %{_bindir}/xscreensaver
#%%{_bindir}/xscreensaver-systemd
%{_bindir}/xscreensaver-command
%{_bindir}/xscreensaver-demo
%{_bindir}/xscreensaver-settings
%{_bindir}/dmctl
%{_datadir}/pixmaps/*
#{_datadir}/fonts/%{name}/OCRAStd.otf
%{_datadir}/fonts/%{name}/SpecialElite.ttf
%{_datadir}/fonts/%{name}/clacon.ttf
%{_datadir}/fonts/%{name}/gallant12x22.ttf
%{_datadir}/fonts/%{name}/luximr.ttf
%{_iconsdir}/hicolor/*/apps/*.png

%files common
%{_datadir}/X11/app-defaults/*
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/xscreensaver-auth
%{_libexecdir}/%{name}/xscreensaver-gfx
%{_libexecdir}/%{name}/xscreensaver-systemd
%{_datadir}/applications/xscreensaver-settings.desktop
%{_datadir}/applications/xscreensaver.desktop
%{_datadir}/xscreensaver/xscreensaver.service
%doc %{_mandir}/man1/xscreensaver-settings*
%doc %{_mandir}/man6/xscreensaver-auth*
%doc %{_mandir}/man6/xscreensaver-gfx*
%doc %{_mandir}/man6/xscreensaver-systemd*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/config
%{_datadir}/%{name}/config/README

%files base -f base.files
%{_sbindir}/update-xscreensaver-hacks

%files gl -f gl-extras.files
%doc README.GL
