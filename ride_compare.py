import gpxpy
import argparse
from matplotlib import pyplot as plt, gridspec, animation
import numpy as np
import datetime
import math

def create_argument_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filename', default=None, nargs='+',
                        help='the file names of gpx files')
    parser.add_argument('--startloc', type=float, default=None, nargs=2,
                        help='the start location by latitude, longitude')
    parser.add_argument('--endloc', type=float, default=None, nargs=2,
                        help='the end location by latitude, longitude')
    parser.add_argument('--speed', type=int, default=60,
                        help='the playback speed')
    parser.add_argument('--save', action='store_true',
                        help='toggle to save animation')
    return parser

def lldist2d(origin, destination):
    '''
    Compute the 2d distance based on the latitude and longitude of two points.
    
    Args:
        origin, destination (tuples of floats): (latitude, longitude).
        
    Return:
        2-d distance (ignoring elevation) in kilometers.
    
    '''
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d
    
def dist2d(p0, p1):
    '''
    Compute Euclidean distance between two coordinates.
    '''
    return math.sqrt((p1[0] - p0[0])**2 + (p1[0] - p0[0])**2)

def read_gpx(file_name, start_loc, end_loc):
    with open(file_name, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        data = []
        for track in gpx.tracks:
            for segment in track.segments:
                pos = (segment.points[0].latitude, segment.points[0].longitude)
                dist = 0
                for point in segment.points:
                    dist += lldist2d(pos, (point.latitude, point.longitude))
                    pos = (point.latitude, point.longitude)
                    data.append((point.time, point.latitude, point.longitude, dist, point.elevation))                    
        data = np.array(data)        
        if start_loc:
            dists = []
            for dat in data:
                dists.append(dist2d(dat[1:3], start_loc))
            start = np.argmin(dists)
        else:
            start = 0
        if end_loc:
            dists = []
            for dat in data:
                dists.append(dist2d(dat[1:3], end_loc))
            end = np.argmin(dists)
        else:
            end = len(data)
    return data[start:end] - data[start]

def play(trajs, names, speed, save):
    # Create the figure
    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=1, width_ratios=[2, 1])
    
    # Create trajectory plot
    ax0 = fig.add_subplot(spec[0])
    ax0.set_xlabel('longitude')
    ax0.set_ylabel('latitude')
    ax0.set_title('Tracks')
    ax0.set_aspect('equal')
    locs = []
    for name, traj in zip(names, trajs):
        ax0.plot(traj[:, 2], traj[:, 1], label=name)
        c = ax0.get_lines()[-1].get_color()
        loc, = ax0.plot(traj[0, 2], traj[0, 1], 'o', color=c)
        locs.append(loc)
    
    # Create elevation plot
    ax1 = fig.add_subplot(spec[1])
    ax1.set_xlabel('2d distance (km)')
    ax1.set_ylabel('elevation (m)')
    ax1.set_title('Elevation')
    eles = []
    for name, traj in zip(names, trajs):
        ax1.plot(traj[:, 3], traj[:, 4], label=name)
        c = ax1.get_lines()[-1].get_color()
        ele, = ax1.plot(traj[0, 3], traj[0, 4], 'o', color=c)
        eles.append(ele)
    
    def animate(i):
        for loc, ele, traj in zip(locs, eles, trajs):
            if i >= len(traj):
                return locs + eles
            else:
                loc.set_data(traj[i, 2], traj[i, 1])
                ele.set_data(traj[i, 3], traj[i, 4])
        return locs + eles
        
    frames = max([len(traj) for traj in trajs])
    # interval (float): The pause between two frames in millisecond.
    interval = (trajs[0][1, 0] - trajs[0][0, 0]).total_seconds() * 1000 / speed
    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=interval, blit=True)
    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
        # installed.  The extra_args ensure that the x264 codec is used, so that
        # the video can be embedded in html5.  You may need to adjust this for
        # your system: for more information, see
        # http://matplotlib.sourceforge.net/api/animation_api.html
    if save:
        anim.save('compare_ride.mp4')
    plt.show()
    
def main():
    args = create_argument_parser().parse_args()
    trajs = []
    for f in args.filename:
        trajs.append(read_gpx(f, args.startloc, args.endloc))
    play(trajs, args.filename, args.speed, args.save)
    
    
if __name__ == '__main__':
    main()
